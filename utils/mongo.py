from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database


class MongoData:
    Title = 'title'
    Link = 'link'
    Time = 'time'


def update_mongo(database: Database, collection_name: str, data: DataFrame) -> str:
    # Initialize an empty message string
    message: str = ''

    # Get the 'collection_name' collection within database
    collection = database[collection_name]

    # Delete documents from the collection where the 'Title' field is not in the provided data
    print(f'Updating collection {collection_name}...')
    query = {MongoData.Title: {'$nin': data[MongoData.Title].to_list()}}
    for itm_to_delete in collection.find(query):
        collection.delete_one(itm_to_delete)

    # Iterate over the data DataFrame
    counter = 0
    for r, title in enumerate(data[MongoData.Title]):
        # Find and update a document in the collection based on the 'Title' field
        if collection.find_one_and_update(
                {MongoData.Title: title},
                {'$set': {MongoData.Time: data[MongoData.Time][r]}}
        ) is None:
            # Increase the counter
            counter += 1
            # If the document doesn't exist, insert a new document into the collection
            collection.insert_one(dict(zip(data.columns, data.values[r])))
            # Append a message with the title and link to the inserted document
            message += f"\"{data[MongoData.Title][r]}\": {data[MongoData.Link][r]}\n"

    # Return the message containing information about inserted documents
    print(f'Update completed: {counter} inserted documents')
    return message


if __name__ == '__main__':
    # Create an empty DataFrame
    df = DataFrame()

    # Populate the DataFrame with test data
    df[MongoData.Title] = ["Test title 1", "Test title 2", "Test title 4"]
    df[MongoData.Link] = ["www.nothing.xx", "https:/www.nothing2.xx", "www.nothing3.xxxx"]
    df[MongoData.Time] = ["updated 20 minutes ago", "updated 16 minutes ago", "recently"]

    # Establish a connection to the MongoDB cluster
    from config.helpers import get_mongo_cluster
    cluster: MongoClient = MongoClient(get_mongo_cluster())

    # Print the result of the 'update_mongo' function with the test data
    print(update_mongo(cluster['News'], 'Bloomberg', df))
