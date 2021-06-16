from prefect import task, Task, Flow
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
import prefect
from timelogs.database import TimeStamps, Database
from timelogs.message import Message
from typing import Any, Dict, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

engine = create_engine('sqlite:///sqlalchemy.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

TEST = [{'timelog_name': 'test',
         'start_time': '0:00',
         'end_time': '10:00',
         'project_name': 'test',
         'employee': 'test',
         'user': 'user',
         'ts': '1622909735.001234'}]

@task
def get_latest_timestamps():
    db = Database(messages=TEST)
    last_ts_db = db.select_last_timestamp()
    return float(last_ts_db)

@task
def retrive_messages(ts_from_db: float=1522909733.001234):
    with open('home/token.json') as json_file:
    # with open('./token.json') as json_file:
        token_dict = json.load(json_file)
    token = token_dict['SLACK_TOKEN']
    client = WebClient(token=token)
    logger = prefect.context.get("logger")
    channel_name = "learning"
    conversation_id = None
    result = client.conversations_list()
    try:
        for response in result:
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    conversation_id = channel["id"]
                    print(f"For channel #{channel_name} found conversation ID: {conversation_id}")
                    break
    except SlackApiError as e:
        print(f"Error: {e}")
    channel_id = "C02327JDKAS"
    try:
        result = client.conversations_history(channel=channel_id)
        conversation_history = result["messages"]
        for message in conversation_history:
            ts_from_message = message['ts']
            if float(ts_from_message) >= ts_from_db:
                logger.info("{} messages found in {}".format(len(conversation_history), id))
                return conversation_history
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))
        return None

@task
def parse_messages(messages: List[str] = None):
    records = []
    for message in messages:
        text = message['text']
        user = message['user']
        timestamp = message['ts']
        msg = Message(text=text, user=user, ts=timestamp)
        record = msg.to_records()
        if record:
            logger = prefect.context.get("logger")
            logger.info(f"New record: {record}")
            records.append(record)
    return records

@task
def insert_into_db(records: List[str] = None):
    for record in records:
        db = Database(messages=record)
        db.insert_into()

with Flow('Slack messages') as flow:
    ts_latest = get_latest_timestamps()
    messages = retrive_messages(ts_latest)
    timelogs = parse_messages(messages)
    add_to_database = insert_into_db(timelogs)


flow.run()
