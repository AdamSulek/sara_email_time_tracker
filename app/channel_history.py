import prefect
from prefect import Task
from typing import Any, Dict
from .message import Message
from .database import Database


class ChannelHistory(Task):
    """
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


    def run(self):

        for message in self.messages:
            msg = Message(text=message['text'], user=message['user'])
            record = msg.to_records()
            logger = prefect.context.get("logger")
            logger.info(f"New record: {record}")
            # here I chekced if record from single message is not empty
            if record:
                db = Database(timelogs=record)
                db.insert_into()
            else:
                logger.info(f"There is no record")

        return True
