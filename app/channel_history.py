import prefect
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
    def __init__(self, *args, messages: Dict[str, Any] = None, **kwargs):
        super().__init__(name="ChannelHistory", *args, **kwargs)
        self.messages = messages
        self.records = []
        #self.message = self.messages[0]['text']
        #self.user = self.messages[0]['user']

    def run(self):

        for message in self.messages:
            msg = Message(text=message['text'], user=message['user'])
            record = msg.to_records()
            logger = prefect.context.get("logger")
            if record:
                db = Database(timelogs=record)
                db.insert_into()
                logger.info(f"New record: {record}")
            else:
                logger.info(f"There is no record")
            
        return True

    # def to_records(self):
    #     for message in self.messages:
    #         msg = Message(text=message['text'], user=message['user'])
    #         rec = msg.to_records()
    #         if rec != [] and db.check_duplicates:
    #             self.records.append(rec)
    #     return self.records
    #
    # def to_database(self):
    #     if self.records == []:
    #         self.to_records()
    #     for record in self.records:
    #         db = Database(record)
    #         db.insert()
    #
    #     return True
