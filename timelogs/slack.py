from sqlalchemy.orm import Session, scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData,\
                       Table, Column, Integer, String, Float, Date, ForeignKey
from typing import Any, Dict, List
from sqlalchemy import func
import logging
import prefect
import datetime
from .source import TimeLogs, MasterDb, TimeStamps, Source


class Slack(Source):
    """
    This class represents

    Parameters
    ----------
    timelogs: List[str], optional
        The timelogs dict from text message.
        by default None
    database_name: str, optional
        by default sqlalchemy.db will be created in root directory.
    """
    def __init__(self, *args, messages: Dict[str, Any] = None, timestamp: float = None, **kwargs):
        super().__init__(name="Slack", *args, **kwargs)
        self.messages = messages
        self.ts = timestamp


    def add_timestamp_to_db(self):
        '''
            This function allow to add timestamp in flow task, for messages which
            are not in a timelog
        '''
        self.DBSession.add(TimeStamps(timestamp=self.ts))
        self.DBSession.commit()


    def insert_into(self):
        for message in self.messages:
            print("jeste w insert_into\n message: {}".format(message))
            if not self.check_duplicates(user=message['user'], start_time=message['start_time'],
                                                               date_time=message['date']):
                self.DBSession.add(TimeLogs(
                                       start_time=message['start_time'],
                                       end_time=message['end_time'],
                                       project_name=message['project_name'],
                                       user=message['user'],
                                       date=message['date'],
                                       h=message['h']
                                       ))
                self.DBSession.commit()

                print("class Database - method: insert_into\nTHIS IS NOT A DUPLICATE!!!!")
            else:
                print("class Database - method: insert_into\nAWARE - THIS IS A DUPLICATE!!!!")


    def select_timestamps(self):
        table_record = []
        sql_select_query = self.DBSession.query(TimeStamps).all()
        for row in sql_select_query:
            table_record.append(row.timestamp)
        return table_record

    def select_last_timestamp_by_max(self):
        '''
            Select calculated last timestamp
        '''
        last_timestamp = self.DBSession.query(func.max(TimeStamps.timestamp)).scalar()
        return last_timestamp

    def select_last_timestamp(self):
        '''
            Select last timestamp by last record in table
        '''
        last_timestamp = self.DBSession.query(TimeStamps).order_by(TimeStamps.id.desc()).first()
        return last_timestamp.timestamp
