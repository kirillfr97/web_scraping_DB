import os

from .settings import *


class NoEnvironmentVar(Exception):
    def __init__(self, variable: str, *args, **kwargs):
        super().__init__(f'Environment variable {variable} does not exist')


def _get_env_variable(variable: str):
    """Retrieve the value of the specified environment variable.

    Args:
        variable (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        NoEnvironmentVar: If the specified environment variable does not exist.

    """
    # Check if the 'variable' environment variable exists
    if variable not in os.environ:
        raise NoEnvironmentVar(variable)

    return os.environ.get(variable)


def get_mongo_url() -> str:
    """Retrieve the MongoDB URL from environment variables.

    Returns:
        str: The MongoDB URL.

    Raises:
        NoEnvironmentVar: If the MONGO_URL environment variable does not exist.

    """
    return _get_env_variable(MONGO_URL)


def get_mongo_database() -> str:
    """Retrieve the MongoDB database name from environment variables.

    Returns:
        str: The MongoDB database name.

    Raises:
        NoEnvironmentVar: If the MONGO_DATABASE_NAME environment variable does not exist.

    """
    return _get_env_variable(MONGO_DATABASE_NAME)


def get_time_interval() -> int:
    """Retrieve the time interval from environment variables.

    Returns:
        int: The time interval.

    Raises:
        NoEnvironmentVar: If the TIME_INTERVAL environment variable does not exist.

    """
    return int(_get_env_variable(TIME_INTERVAL))


def get_slack_token() -> str:
    """Retrieve the Slack bot token from environment variables.

    Returns:
        str: The Slack bot token.

    Raises:
        NoEnvironmentVar: If the SLACK_BOT_TOKEN environment variable does not exist.

    """
    return _get_env_variable(SLACK_BOT_TOKEN)


def get_slack_channel() -> str:
    """Retrieve the Slack channel from environment variables.

    Returns:
        str: The Slack channel.

    Raises:
        NoEnvironmentVar: If the SLACK_CHANNEL environment variable does not exist.

    """
    return _get_env_variable(SLACK_CHANNEL)
