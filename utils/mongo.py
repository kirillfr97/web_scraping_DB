from typing import Optional
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database

from config.helpers import get_mongo_url, get_mongo_database, get_mongo_setup


class MongoData:
    Title = 'title'
    Link = 'link'
    Time = 'time'


class MongoDataBase:
    def __init__(self):
        """Initialize the MongoDataBase class."""
        # List to store information about inserted documents
        self._documents: list = []

        # MongoDB cluster connection object
        self._cluster: Optional[MongoClient] = None

        # Establish a connection to the MongoDB cluster upon initialization
        self._connect()

    def _connect(self):
        """Connect to the MongoDB cluster."""
        try:
            print('Connecting to Database...')

            # Getting the MongoDB cluster URL
            cluster_url = get_mongo_url()

            # Establish a connection to the MongoDB cluster
            self._cluster: MongoClient = MongoClient(cluster_url)

            # Low cost check to verify the availability of the MongoDB server
            self._cluster.admin.command('ping')

        except Exception as e:
            self._cluster = None
            print(repr(e))

    def update(self, data: DataFrame, collection_name: str):
        """Update the collection with the provided data.

        Args:
            data (DataFrame): The data to update the collection with.
            collection_name (str): The name of the collection to update.

        Raises:
            Exception: If no MongoDB cluster connection was established.

        """
        if self._cluster is None:
            raise Exception('No MongoDB cluster connection was established')

        # Clear list of updated documents
        self._documents = []

        # If no data were given then exit without updating
        if data.empty:
            return

        # Get the 'collection_name' collection within database
        collection = self.database[collection_name]

        # Delete documents from the collection where the 'Title' field is not in the provided data
        print(f'Updating collection {collection_name}...')
        query = {MongoData.Title: {'$nin': data[MongoData.Title].to_list()}}
        for itm_to_delete in collection.find(query):
            collection.delete_one(itm_to_delete)

        # Iterate over the data DataFrame
        for r, title in enumerate(data[MongoData.Title]):
            # Find and update a document in the collection based on the 'Title' field
            if collection.find_one_and_update(
                    {MongoData.Title: title},
                    {'$set': {MongoData.Time: data[MongoData.Time][r]}}
            ) is None:
                # If the document doesn't exist, insert a new document into the collection
                collection.insert_one(dict(zip(data.columns, data.values[r])))
                # Append a new document to the list
                self._documents.append([data[MongoData.Title][r], data[MongoData.Link][r]])

        # Return the message containing information about inserted documents
        print(f'Update completed: inserted {len(self._documents)} new documents')

    @property
    def setup_file(self) -> dict:
        """This property retrieves the setup file from the MongoDB database, which contains information
        about the scraped websites.

        Note: 'find_one' is generally considered to be less costly compared to operations like 'find' or 'aggregate' that
        return multiple documents. The performance of the `find_one` operation can vary depending on factors such as the
        size of the collection, the complexity of the query, the presence of indexes, and the network latency
        between the client and the MongoDB server. If there are appropriate indexes on the queried fields,
        the operation can be quite efficient.

        Returns:
            Dict: Setup file which contains information about scraped websites.

        """
        if self.database is not None:
            print('Reading setup file from MongoDB...')
            setup = self.database[get_mongo_setup()].find_one()
            del setup['_id']  # Delete unnecessary key
            print(f'Found {len(setup)} websites to scrape')
            return setup
        return {}

    @property
    def database(self) -> Optional[Database]:
        """Get the MongoDB database object.

        Returns:
            Optional[Database]: The MongoDB database object.

        """
        if self._cluster is not None:
            return self._cluster[get_mongo_database()]
        return None

    @property
    def message(self) -> str:
        """Get the message containing information about inserted documents.

        Returns:
            str: The message containing information about inserted documents.

        """
        if len(self._documents) != 0:
            return ''.join([f'\"{el[0]}\": {el[1]}\n' for el in self._documents])
        return ''

    def close(self):
        """Close the connection to the MongoDB cluster."""
        if self._cluster is not None:
            self._cluster.close()


if __name__ == '__main__':
    # Create an empty DataFrame
    df = DataFrame()

    # Populate the DataFrame with test data
    df[MongoData.Title] = ['Test title 1', 'Test title 2', 'Test title 4']
    df[MongoData.Link] = ['www.nothing.xx', 'https:/www.nothing2.xx', 'www.nothing3.xxxx']
    df[MongoData.Time] = ['updated 20 minutes ago', 'updated 16 minutes ago', 'recently']

    try:
        # Establish a connection to the MongoDB cluster
        cluster = MongoDataBase()

        # Update the MongoDB database with the scraped data and retrieve the message
        cluster.update(data=df, collection_name='Test')

        # Print the result of the 'update' function with the test data
        print(cluster.message)

    except Exception as error:
        print(repr(error))
