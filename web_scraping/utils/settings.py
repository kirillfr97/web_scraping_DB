from json import load
from os import path
from typing import Any, Dict, List

from pymongo.database import Collection


class SettingsFileError(Exception):
    pass


def get_settings_from_collection(name: str, field: str, collection: Collection) -> List[Dict[str, Any]]:
    """This function retrieves settings document from the database.

    Args:
        name (str): The name of the settings file.
        field (str): The name of the settings field.
        collection (Collection): The collection in Database with settings file.

    Returns:
        Dict: Information about scraped websites.

    Raises:
        SettingsFileError: If there is no file or the structure of the file is wrong.

    """
    # Get settings document from the given collection
    settings = collection.find_one({'name': name})

    if settings is None:
        raise SettingsFileError(f'No settings file with {name = } were found in collection \"{collection.full_name}\"')

    # Read settings file and extract data
    data = settings.get('data', {}).get(field, None)
    if data is None:
        raise SettingsFileError(f'No {field = } in the file {name} of collection \"{collection.full_name}\"')

    # Filter according to enable key-field
    return [d for d in data if d.get('enable', True)]


def get_settings_from_local(file_path: str) -> List[Dict[str, Any]]:
    """This function retrieves file from the local machine, which contains information about the scraped websites.

    Args:
        file_path (str): The path to the file.

    Returns:
        Dict: Information about scraped websites.

    Raises:
        SettingsFileError: If there is no file or the structure of the file is wrong.

    """
    if not path.exists(file_path):
        raise SettingsFileError(f'Nothing were found on path {file_path}')

    if not path.isfile(file_path):
        raise SettingsFileError(f'{file_path} is not a file')

    data = []
    _, extension = path.splitext(file_path)
    if extension == '.json':
        # Read the contents of the JSON file
        with open(file_path, "r") as file:
            data = load(file)
    elif extension == '.txt':
        # Read the contents of the JSON file
        with open(file_path, "r") as file:
            data = file.read()
    return data
