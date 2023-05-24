import json


def load_config(file_path: str):
    # This function loads a JSON configuration file and returns the parsed data
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def get_slack_token(file_path: str) -> str:
    # This function retrieves the Slack OAuth token from a configuration file
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
        return config['slack']['oauth_token']


def get_slack_channel(file_path: str) -> str:
    # This function retrieves the Slack Channel from a configuration file
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
        return config['slack']['channel']


def get_mongo_cluster(file_path: str) -> str:
    # This function retrieves the MongoDB cluster connection URL from a configuration file
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
        login = config['mongo_db']['login']
        password = config['mongo_db']['password']
    return f'mongodb+srv://{login}:{password}@freecluster.apw2jua.mongodb.net/'
