import os

# This is Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# This is Configuration File Path
CONFIG_PATH = os.path.join(ROOT_DIR, 'config', 'slack_cfg.json')

# This is a name of Environment Variable
SLACK_BOT_TOKEN = "SLACK_BOT_TOKEN"

# Specifying the frequency of code execution (in seconds)
TIME_INTERVAL = 5000
