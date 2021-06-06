from typing import Any, Dict
from .message import Message
from .database import Database


class ChannelHistory:
    """
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


    def channel_to_records(self):
        for message in self.messages:
            msg = Message(text=message['text'], user=message['user'])
            rec = msg.to_records()
            if rec != []:
                self.records.append(rec)
        return self.records

    def channel_to_database(self):
        for record in self.records:
            msg_to_db = Database(record)
            msg_to_db.insert_bulk()

        return True
