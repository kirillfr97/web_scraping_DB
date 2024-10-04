import pytest

from web_scraping.utils.database.wrapper import DBWrapper


@pytest.fixture(scope="session")
def connect_db() -> DBWrapper:
    """Connect to Database before tests, disconnect after."""
    #  Setup: establish a connection to MongoDB
    cluster = DBWrapper()

    assert cluster.main_collection is not None
    assert cluster.issue_collection is not None
    assert cluster.settings_collection is not None

    # Testing
    yield cluster

    # Teardown: stop Database
    cluster.close()
