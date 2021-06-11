import logging
import os
import json
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
TOKEN = "xoxb-2055296280309-2146683809428-EUxKty9ne2jvWtwlSFP2XGy7"

class DownloadSlack:
    def __init__(self, token_: str = TOKEN, name: str = "learning", channel_id: str = "C02327JDKAS"):
        self.client = WebClient(token=token_)
        self.logger = logging.getLogger(__name__)
        self.channel_name = name
        self.conversation_id = None
        self.channel_id = channel_id
        self.conversations_list()


    def conversations_list(self):
        result = self.client.conversations_list()
        try:
            # Call the conversations.list method using the WebClient
            for response in result:
                if self.conversation_id is not None:
                    break
                for channel in result["channels"]:
                    if channel["name"] == channel_name:
                        self.conversation_id = channel["id"]
                        #Print result
                        print(f"For channel #{channel_name} found conversation ID: {conversation_id}")
                        break
        except SlackApiError as e:
            print(f"Error: {e}")

    # timestamp - from TimeStamps table
    def get_messages(self, timestamp: str = None):
        try:
            result = client.conversations_history(channel=self.channel_id)
            if int(result["ts"]) > int(timestamp):
                conversation_history = result["messages"]
                # Print results
                logger.info("{} messages found in {}\n result[ts]: {}".format(len(conversation_history), id, result["ts"]))
        except SlackApiError as e:
            logger.error("Error creating conversation: {}".format(e))

        return conversation_history


    def run(self):


# FROM_FILE = conversation_history
#
# with open("messages.json", 'w') as out_file:
#     out = json.dumps(conversation_history)
#     out_file.write(out)
