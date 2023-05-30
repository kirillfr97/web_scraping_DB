import os
from json import load

from definitions import CONFIG_PATH


def load_config() -> dict:
    # Check if the configuration file exists
    if not os.path.exists(CONFIG_PATH):
        return {}

    # Open the configuration file and load the JSON data
    with open(CONFIG_PATH, 'r') as config_file:
        config: dict = load(config_file)

    return config


def get_slack_token() -> str:
    # This function retrieves the Slack OAuth token from a configuration file
    config = load_config()

    # If configuration is not available, return an empty string
    return config.get('slack', {}).get('oauth_token', '')


def get_slack_channel() -> str:
    # This function retrieves the Slack Channel from a configuration file
    config = load_config()

    # If configuration is not available, return an empty string
    return config.get('slack', {}).get('channel', '')


def get_mongo_cluster() -> str:
    # This function retrieves the MongoDB cluster connection URL from a configuration file
    config = load_config()

    login = config.get('mongo_db', {}).get('login', '')
    password = config.get('mongo_db', {}).get('password', '')
    return f'mongodb+srv://{login}:{password}@freecluster.apw2jua.mongodb.net/'
