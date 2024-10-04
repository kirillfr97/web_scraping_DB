from pymongo import MongoClient
from pymongo.database import Collection

from web_scraping.config import CLUSTER_URL, get_env_variable


class MongoError(Exception):
    pass


class MongoDB:
    def __init__(self):
        """Initialize the MongoDataBase class."""
        # Getting the MongoDB cluster URL
        cluster_url = get_env_variable(CLUSTER_URL)

        # Establish a connection to the MongoDB cluster
        self._client = MongoClient(cluster_url)

        # Low cost check to verify the availability of the MongoDB server
        self._client.admin.command('ping')

    def get(self, database_name: str, collection_name: str) -> Collection:
        """Get specified collection from the MongoDB database."""
        return self._client[database_name][collection_name]

    def close(self):
        """Close the connection to the MongoDB cluster."""
        if self._client is not None:
            self._client.close()
