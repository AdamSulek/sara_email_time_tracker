import logging
import os
import json
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token="xoxb-2055296280309-2146683809428-1ZmC4d5o03s0LSFERkO9u4xU")
logger = logging.getLogger(__name__)
channel_name = "learning"
conversation_id = None
result = client.conversations_list()
try:
    # Call the conversations.list method using the WebClient
    for response in result:
        if conversation_id is not None:
            break
        for channel in result["channels"]:
            if channel["name"] == channel_name:
                conversation_id = channel["id"]
                #Print result
                print(f"For channel #{channel_name} found conversation ID: {conversation_id}")
                break
except SlackApiError as e:
    print(f"Error: {e}")
channel_id = "C02327JDKAS"
try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id)
    conversation_history = result["messages"]
    # Print results
    logger.info("{} messages found in {}".format(len(conversation_history), id))
except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))

FROM_FILE = conversation_history

with open("messages.json", 'w') as out_file:
    out = json.dumps(conversation_history)
    out_file.write(out)
