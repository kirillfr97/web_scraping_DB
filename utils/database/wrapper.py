from typing import Optional

from pandas import DataFrame
from pymongo.database import Collection

from web_scraping.config import (
    ISSUES_COLLECTION,
    ISSUES_DATABASE,
    ISSUES_TTL_VALUE,
    MAIN_COLLECTION,
    MAIN_DATABASE,
    MAIN_TTL_VALUE,
    SETTINGS_COLLECTION,
    SETTINGS_DATABASE,
    get_env_variable,
)
from web_scraping.log import log
from web_scraping.scrapers.base_scraper import BaseScraper
from web_scraping.utils import DataFields, IssueFields
from web_scraping.utils.database import MongoDB, MongoError


# Define name for TTL index
TTL_IDX_NAME = 'ttl_idx'

# Define name for HASH index
HASH_IDX_NAME = 'hash_idx'


class DBWrapper(MongoDB):
    def __init__(self):
        """Initialize the MongoDataBase class."""
        super().__init__()

        # MongoDB's collection object
        self._main_collection: Optional[Collection] = None
        self._issue_collection: Optional[Collection] = None
        self._settings_collection: Optional[Collection] = None

        # Establish a connection to the MongoDB cluster upon initialization
        self._connect()

    def _connect(self):
        """Connect to the MongoDB cluster."""
        try:
            log.info('Connecting to Database')

            # Getting the MongoDB TTL value
            main_ttl_value = int(get_env_variable(MAIN_TTL_VALUE))
            issue_ttl_value = int(get_env_variable(ISSUES_TTL_VALUE))

            # Getting the MongoDB database names
            main_database_name = get_env_variable(MAIN_DATABASE)
            issue_database_name = get_env_variable(ISSUES_DATABASE)
            settings_database_name = get_env_variable(SETTINGS_DATABASE)

            # Getting the MongoDB collection names
            main_collection_name = get_env_variable(MAIN_COLLECTION)
            issue_collection_name = get_env_variable(ISSUES_COLLECTION)
            settings_collection_name = get_env_variable(SETTINGS_COLLECTION)

            # Get collections to work with
            self._main_collection = self._client[main_database_name][main_collection_name]
            self._issue_collection = self._client[issue_database_name][issue_collection_name]
            self._settings_collection = self._client[settings_database_name][settings_collection_name]

            # Create or update HASH index for the given fields
            self._create_or_update_index(self._main_collection, HASH_IDX_NAME, DataFields.HashID, unique=False)

            # Create or update TTL index for the given fields
            self._create_or_update_index(self._main_collection, TTL_IDX_NAME, DataFields.Created, expireAfterSeconds=main_ttl_value)
            self._create_or_update_index(self._issue_collection, TTL_IDX_NAME, IssueFields.Created, expireAfterSeconds=issue_ttl_value)

        except Exception as error:
            from traceback import format_exc

            log.error(format_exc(), console=False, slack=False)
            log.error(repr(error), store=False)
            self.close()

    @staticmethod
    def _create_or_update_index(collection: Collection, idx_name: str, idx_field: str, **options):
        # Get info about index
        idx_info = collection.index_information().get(idx_name, None)

        if idx_info is None:
            collection.create_index(idx_field, name=idx_name, **options)
        elif idx_name == TTL_IDX_NAME and idx_info.get('expireAfterSeconds') != options.get('expireAfterSeconds'):
            collection.drop_index(index_or_name=idx_name)
            collection.create_index(idx_field, name=idx_name, **options)

    @property
    def main_collection(self) -> Optional[Collection]:
        """Property to return collection, where main data is stored."""
        return self._main_collection

    @property
    def issue_collection(self) -> Optional[Collection]:
        """Property to return collection, where all issue reports are stored."""
        return self._issue_collection

    @property
    def settings_collection(self) -> Optional[Collection]:
        """Property to return collection, where all settings are stored."""
        return self._settings_collection

    def update_with_scraper(self, scraper: BaseScraper) -> DataFrame:
        """Update the main collection with the provided data.

        Args:
            scraper (BaseScraper): Scraper entity with data to update collection.

        Returns:
            DataFrame: The DataFrame containing information about inserted documents.

        Raises:
            MongoError: If no cluster connection was established.

        """
        if self._client is None or self._main_collection is None:
            raise MongoError('No cluster connection was established')

        # List to store information about inserted documents
        documents = DataFrame(columns=list(DataFields()))

        # If no data were given then exit without updating
        if scraper.data.empty:
            return documents

        # Iterate over the data DataFrame
        for idx, row in scraper.data.iterrows():
            # Find and update a document in the collection based on the 'Title' field
            if (
                self._main_collection.find_one_and_update(
                    {DataFields.HashID: row[DataFields.HashID]}, {'$set': {DataFields.Check: row[DataFields.Check]}}
                )
                is None
            ):
                # If the document doesn't exist, add metadata to this document
                scraper.add_metadata(idx)

        # Get updated documents using mask and insert them to the database
        documents = scraper.data[scraper.data[DataFields.Title] != '']
        if len(documents) > 0:
            self._main_collection.insert_many([doc.to_dict() for _, doc in documents.iterrows()])

        log.debug(f'Update completed: inserted {len(documents)} new documents')
        return documents

    def close(self):
        """Close the connection to the MongoDB cluster."""
        super().close()
        self._client = None
        self._main_collection = None
        self._issue_collection = None
        self._settings_collection = None
