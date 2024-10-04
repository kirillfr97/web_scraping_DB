# This is a name of Environment Variable for the frequency of code execution (in seconds)
TIME_INTERVAL = 'TIME_INTERVAL'

# This is a name of Environment Variable for the name of Slack Channel (which will receive messages)
SLACK_CHANNEL = 'SLACK_CHANNEL'

# This is a name of Environment Variable for the name of Slack Channel (which will receive messages with issues)
SLACK_REPORT_CHANNEL = 'SLACK_REPORT_CHANNEL'

# This is a name of Environment Variable for Slack Token
SLACK_BOT_TOKEN = 'SLACK_BOT_TOKEN'

# This is a name of Environment Variable for maximum number of failed attempts
MAX_FAILED_ATTEMPTS = 'MAX_FAILED_ATTEMPTS'

# This is a name of Environment Variable for MongoDB Cluster URL
CLUSTER_URL = 'CLUSTER_URL'

# This is a name of Environment Variable for MongoDB database's name, where all articles are stored
MAIN_DATABASE = 'MAIN_DATABASE'

# This is a name of Environment Variable for MongoDB collection, where all articles are stored
MAIN_COLLECTION = 'MAIN_COLLECTION'

# This is a name of Environment Variable for MongoDB database's name, where all sources information are stored
SETTINGS_DATABASE = 'SETTINGS_DATABASE'

# This is a name of Environment Variable for MongoDB collection where all sources information are stored
SETTINGS_COLLECTION = 'SETTINGS_COLLECTION'

# This is a name of Environment Variable for name of the settings file, containing all necessary information
SETTINGS_FILE_NAME = 'SETTINGS_FILE_NAME'

# This is a name of Environment Variable for MongoDB database's name, where all issues are stored
ISSUES_DATABASE = 'ISSUES_DATABASE'

# This is a name of Environment Variable for MongoDB collection where all issues are stored
ISSUES_COLLECTION = 'ISSUES_COLLECTION'

# This is a name of Environment Variable for MongoDB data expiration time used for TTL indexes in MAIN_COLLECTION
MAIN_TTL_VALUE = 'MAIN_TTL_VALUE'

# This is a name of Environment Variable for MongoDB data expiration time used for TTL indexes in ISSUES_COLLECTION
ISSUES_TTL_VALUE = 'ISSUES_TTL_VALUE'

# This is a name of Environment Variable for Pusher application ID
PUSHER_APP_ID = 'PUSHER_APP_ID'

# This is a name of Environment Variable for Pusher key
PUSHER_APP_KEY = 'PUSHER_APP_KEY'

# This is a name of Environment Variable for Pusher secret
PUSHER_APP_SECRET = 'PUSHER_APP_SECRET'

# This is a name of Environment Variable for Pusher cluster name
PUSHER_APP_CLUSTER = 'PUSHER_APP_CLUSTER'

# This is a name of Environment Variable for Pusher channel
PUSHER_CHANNEL = 'PUSHER_CHANNEL'

# This is a name of Environment Variable for Pusher event
PUSHER_EVENT = 'PUSHER_EVENT'
