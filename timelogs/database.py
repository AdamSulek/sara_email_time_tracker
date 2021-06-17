from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData, Table, Column, Integer, String, Float
from .message import Message
from typing import Any, Dict, List
from sqlalchemy import func
import logging
import prefect

Base = declarative_base()
DBSession = scoped_session(sessionmaker())
engine = None

class TimeLogs(Base):

    __tablename__ = "timelogs"
    id = Column(Integer, primary_key=True)
    start_time = Column(String)
    end_time = Column(String)
    project_name = Column(String)
    user = Column(String)


class TimeStamps(Base):

    __tablename__ = "timestamps"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)


class Database:
    """
    This class represents Database with initialize db connection,
    insert_bulk and select_query methods.

    Parameters
    ----------
    timelogs: List[str], optional
        The timelogs list information from text message.
        by default None
    database_name: str, optional
        by default sqlalchemy.db will be created in root directory.
    """
    def __init__(self, messages: List[str] = None, database_name: str = 'metabase', timestamp: float = None):
        logger = prefect.context.get("logger")
        self.messages = messages
        self.database_name = database_name
        POSTGRES_URL = 'postgresql://{}:{}@{}:{}/{}'.format('postgres',        # user
                                                            'postgres',        # password
                                                            'database',        # host name
                                                            '5432',            # port
                                                            self.database_name # database)
                                                            )
        engine = create_engine(POSTGRES_URL)
        DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
        Base.metadata.create_all(engine)
        self.ts = timestamp
        # adding of timestamps of every message - even for message without timelog event
        # for message in self.messages:
        #     ts = float(message['ts'])
        #     logger.info("Added new timestamp: {}".format(ts))
        #     DBSession.add(TimeStamps(timestamp=ts))
        #     DBSession.commit()

    def add_timestamp_to_db(self):
        '''
            This function allow to add timestamp in flow task, for messages which
            are not a timelog
        '''
        DBSession.add(TimeStamps(timestamp=self.ts))
        DBSession.commit()


    def insert_into(self):
        for message in self.messages:
            if not self.check_duplicates(user=message['user'], start_time=message['start_time']):
                DBSession.add(TimeLogs(
                                       start_time=message['start_time'],
                                       end_time=message['end_time'],
                                       project_name=message['project_name'],
                                       user=message['user']
                                       ))
                DBSession.commit()

                print("class Database - method: insert_into\nTHIS IS NOT A DUPLICATE!!!!")
            else:
                print("class Database - method: insert_into\nAWARE - THIS IS A DUPLICATE!!!!")


    def insert_bulk(self):
        DBSession.bulk_insert_mappings(
            TimeLogs,
            [
                timelog for timelog in self.messages
            ]
        )
        DBSession.commit()

        return True

    def select_timestamps(self):
        table_record = []
        sql_select_query = DBSession.query(TimeStamps).all()
        for row in sql_select_query:
            table_record.append(row.timestamp)
        return table_record

    def select_last_timestamp_by_max(self):
        '''
            Select calculated last timestamp
        '''
        # session.query(self.stats.c.ID, func.max(self.stats.c.STA_DATE))
        last_timestamp = DBSession.query(func.max(TimeStamps.timestamp)).scalar()
        return last_timestamp

    def select_last_timestamp(self):
        '''
            Select last timestamp by last record in table
        '''
        last_timestamp = DBSession.query(TimeStamps).order_by(TimeStamps.id.desc()).first()
        return last_timestamp.timestamp


    def select_all_timelogs(self):
        table_record = []
        sql_select_query = DBSession.query(TimeLogs).all()
        for row in sql_select_query:
            table_record.append((row.id,
                                 row.start_time,
                                 row.end_time,
                                 row.project_name,
                                 row.user))

        return table_record


    def check_duplicates(self, user, start_time):
        '''
            This function filter duplicates of timelog define as
            the same user and the same start_time in TimeLogs Table.
        '''
        filter = DBSession.query(TimeLogs).filter_by(user=user, start_time=start_time).first()
        # print("class Database - method: check_duplicates\nuser: {}\n start_time: {}\n filter: {}".format(user,
        #                                                                                         start_time,
        #                                                                                         filter))
        if filter:
            print("You are stupid!!!\n this Timelog was created by You")
            return True
        print("You create new Timelog")
        return False
