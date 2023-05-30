import os
from typing import Optional

from .settings import *


def get_mongo_cluster() -> Optional[str]:
    # Check if the MONGO_LOGIN environment variable exists
    if MONGO_LOGIN not in os.environ:
        print(f'Environment variable {MONGO_LOGIN} does not exist')
        return None

    # Check if the MONGO_PASSWORD environment variable exists
    if MONGO_PASSWORD not in os.environ:
        print(f'Environment variable {MONGO_PASSWORD} does not exist')
        return None

    # Retrieve the values of MONGO_LOGIN and MONGO_PASSWORD from environment variables
    login = os.environ.get(MONGO_LOGIN)
    password = os.environ.get(MONGO_PASSWORD)

    # Construct and return the MongoDB cluster URL
    return f'mongodb+srv://{login}:{password}@freecluster.apw2jua.mongodb.net/'


def get_slack_token() -> Optional[str]:
    # Check if the SLACK_BOT_TOKEN environment variable exists
    if SLACK_BOT_TOKEN not in os.environ:
        print(f'Environment variable {SLACK_BOT_TOKEN} does not exist')
        return None

    # Retrieve the value of SLACK_BOT_TOKEN from environment variables
    return os.environ.get(SLACK_BOT_TOKEN)
