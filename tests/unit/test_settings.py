from typing import Any, Dict, List, Tuple

import pytest

from web_scraping.config import SETTINGS_FILE_NAME, get_env_variable


source_necessary_fields = [
    'name',
    'enable',
    'target_url',
    'crawl_urls',
    'sections',
]

user_agent_necessary_fields = [
    'enable',
    'comment',
    'value',
]

settings_fields = [
    ['sources', source_necessary_fields],
    ['user_agents', user_agent_necessary_fields],
]


@pytest.fixture()
def get_settings(connect_db) -> Tuple:
    # Extract collection
    collection = connect_db.settings_collection

    # Retrieve settings file name
    name = get_env_variable(SETTINGS_FILE_NAME)

    # Get settings document from the given collection
    settings = collection.find_one({'name': name})

    return collection, name, settings


class TestSettings:
    """Class to test the content of the settings file."""

    def test_get_settings(self, get_settings):
        # Extract settings data
        _, name, settings = get_settings

        assert settings is not None, f'No settings file with {name = } were found in collection'

    @pytest.mark.parametrize('data', settings_fields)
    def test_check_settings(self, get_settings, data):
        # Extract settings data
        collection, name, settings = get_settings

        # Read settings file and extract data
        sources: List[Dict[str, Any]] = settings.get('data', {}).get(data[0], None)

        assert sources is not None, f'No {data[0]} field in the file {name} of collection \"{collection.full_name}\"'

        # Checking source file
        for source in sources:
            for field in data[1]:
                assert source.get(field, None) is not None, f'There should be {field = } in settings file'
