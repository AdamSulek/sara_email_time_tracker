from prefect import task, Task, Flow
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
import prefect
from timelogs.database import TimeStamps, Database, Master_db
from timelogs.message import Message
from typing import Any, Dict, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json


@task
def get_latest_timestamps():
    '''
        Output: float
    '''
    db = Database()
    every_ts_db = db.select_timestamps()
    last_ts_db = db.select_last_timestamp_by_max()
    if last_ts_db == None:
        last_ts_db = '1622909735.001234'
    return float(last_ts_db)


@task
def retrive_messages(ts_from_db: float=1522909733.001234):
    '''
        Input: float
        Output: List[Message]
    '''
    with open('home/token.json') as json_file:
    with open('./token.json') as json_file:
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
    print("retrive_messages - last time stamp from db: {}".format(ts_from_db))
    try:
        result = client.conversations_history(channel=channel_id)
        conversation_history = result["messages"]
        logger.info("{} messages found in {}".format(len(conversation_history), id))
        new_messages = []
        for message in conversation_history:
            ts_from_message = message['ts']
            ts = float(ts_from_message)
            if ts >= ts_from_db:
                logger.info("newer message - {}\n content: {}".format(ts, message['text']))
                new_messages.append(message)
                # add newer timestamp even if not a message record
                db = Database(timestamp=ts)
                db.add_timestamp_to_db()
            else:
                logger.info("older message - {}".format(float(ts_from_message)))

        print("new_messages: {}".format(new_messages))
        return new_messages

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))
        return None

@task
def parse_messages(messages: List[str] = None):
    '''
        Input: List[Message]
        Output: List[Message]
    '''
    records = []
    for message in messages:
        text = message['text']
        user = message['user']
        timestamp = message['ts']
        for single_line in text.split('\n'):
            print("single_line: {}".format(single_line))
            #msg = Message(text=text, user=user, ts=timestamp)
            msg = Message(text=single_line, user=user, ts=timestamp)
            record = msg.to_records()
            if record:
                logger = prefect.context.get("logger")
                logger.info(f"New record: {record}")
                records.append(record)
            #check if add me message
            add_me = msg.check_add_me()
            if add_me:
                logger = prefect.context.get("logger")
                logger.info(f"New User: {add_me}")
                db = Database()
                db.insert_into_master_db(id=message['user'], user_name=add_me)

    print("records: {}".format(records))
    return records

@task
def insert_into_db(records: List[str] = None):
    '''
        Input: List[Message]
    '''
    for record in records:
        db = Database(messages=record)
        db.insert_into()


with Flow('Slack messages') as flow:
    ts_latest = get_latest_timestamps()
    messages = retrive_messages(ts_latest)
    timelogs = parse_messages(messages)
    add_to_database = insert_into_db(timelogs)


flow.run()
