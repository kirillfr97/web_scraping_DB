from pusher import Pusher

from web_scraping.config import (
    PUSHER_APP_CLUSTER,
    PUSHER_APP_ID,
    PUSHER_APP_KEY,
    PUSHER_APP_SECRET,
    get_env_variable,
)


def test_pusher_connection():
    # Retrieve environment variables
    app_id = get_env_variable(PUSHER_APP_ID)
    key = get_env_variable(PUSHER_APP_KEY)
    secret = get_env_variable(PUSHER_APP_SECRET)
    cluster = get_env_variable(PUSHER_APP_CLUSTER)
    ssl = True

    # Create pusher object
    pusher = Pusher(app_id=app_id, key=key, secret=secret, cluster=cluster, ssl=ssl)

    # Testing client
    assert pusher._pusher_client.app_id == app_id
    assert pusher._pusher_client.key == key
    assert pusher._pusher_client.secret == secret
    assert pusher._pusher_client.ssl is True
