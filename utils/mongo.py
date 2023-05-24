import pandas as pd

TEST_LOGIN: str = 'kirill'
TEST_PASSWORD: str = '1234'


class MongoData:
    Title = 'title'
    Link = 'link'
    Time = 'time'


def update_mongo(cluster_name: str, data: pd.DataFrame) -> str:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    cluster: MongoClient = MongoClient(cluster_name)

    message: str = ''
    try:
        # Low cost check
        cluster.admin.command('ping')
        # Get DB and collection in it
        database = cluster['News']
        collection = database['Bloomberg']

        # collection.delete_many({})
        print(f'Updating...\nAdding {len(data)} new rows')
        for row in data.to_numpy():
            collection.insert_one(dict(zip(data.columns, row)))
            message += f"\"{row[0]}\": {row[1]}\n"

    except ConnectionFailure:
        print('Server not available')
    except Exception as error:
        print(repr(error))
    finally:
        cluster.close()

    return message


if __name__ == '__main__':
    df = pd.DataFrame()
    df[MongoData.Title] = ["Test title 1", "Test title 2", "Test title 3"]
    df[MongoData.Link] = ["www.nothing.xx", "https:/www.nothing2.xx", "www.nothing3.xxxx"]
    df[MongoData.Time] = ["updated 20 minutes ago", "updated 5 minutes ago", "o"]

    update_mongo(f"mongodb+srv://{TEST_LOGIN}:{TEST_PASSWORD}@freecluster.apw2jua.mongodb.net/", df)
