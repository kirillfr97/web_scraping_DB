from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient

SLACK_CHANNEL: str = "test"
SLACK_BOT_TOKEN: str = "xoxb-5310612778596-5305206526405-PJNrT3HOi0okNo9dLWKnyZMO"


def msg_slack(text: str):
    try:
        client = WebClient(token=SLACK_BOT_TOKEN)
        client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=text)
    except SlackApiError as error:
        print(repr(error))
