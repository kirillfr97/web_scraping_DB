import pandas as pd

from config.helpers import get_mongo_cluster


class MongoData:
    Title = 'title'
    Link = 'link'
    Time = 'time'


def update_mongo(cluster_name: str, data: pd.DataFrame) -> str:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure

    # Initialize an empty message string
    message: str = ''

    if cluster_name == '':
        return message

    # Establish a connection to the MongoDB cluster
    cluster: MongoClient = MongoClient(cluster_name)

    try:
        # Low cost check to verify the availability of the MongoDB server
        cluster.admin.command('ping')

        # Get the 'News' database and the 'Bloomberg' collection within it
        database = cluster['News']
        collection = database['Bloomberg']

        # Delete documents from the collection where the 'Title' field is not in the provided data
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
                # Append a message with the title and link to the inserted document
                message += f"\"{data[MongoData.Title][r]}\": {data[MongoData.Link][r]}\n"

    except ConnectionFailure:
        # Handle connection failure error
        print('Server not available')
    except Exception as error:
        # Handle other exceptions
        print(repr(error))
    finally:
        # Close the connection to the MongoDB cluster
        cluster.close()

    # Return the message containing information about inserted documents
    return message


if __name__ == '__main__':
    # Create an empty DataFrame
    df = pd.DataFrame()

    # Populate the DataFrame with test data
    df[MongoData.Title] = ["Test title 1", "Test title 2", "Test title 4"]
    df[MongoData.Link] = ["www.nothing.xx", "https:/www.nothing2.xx", "www.nothing3.xxxx"]
    df[MongoData.Time] = ["updated 20 minutes ago", "updated 16 minutes ago", "recently"]

    # Print the result of the 'update_mongo' function with the test data
    print(update_mongo(get_mongo_cluster(), df))
