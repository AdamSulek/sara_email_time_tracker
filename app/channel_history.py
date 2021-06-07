from prefect import Task
from typing import Any, Dict
from .message import Message
from .database import Database


class ChannelHistory(Task):
    """
    Task???
    A class parsing timelog information from messages history.

    Parameters
    ----------
    messages: Dict[str, Any], optional
        The parameter with information from text message.
        by default None
    """
    def __init__(self, messages: Dict[str, Any] = None):
        self.messages = messages
        self.records = []


    def to_records(self):
        for message in self.messages:
            msg = Message(text=message['text'], user=message['user'])
            rec = msg.to_records()
            if rec != [] and db.check_duplicates:
                self.records.append(rec)
        return self.records

    def to_database(self):
        if self.records == []:
            self.to_records()
        for record in self.records:
            db = Database(record)
            db.insert()

        return True
