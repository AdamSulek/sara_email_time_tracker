from sqlalchemy.orm import Session, scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData,\
                       Table, Column, Integer, String, Float, Date, ForeignKey
from typing import Any, Dict, List
from sqlalchemy import func
import logging
import prefect
import datetime
from abc import abstractmethod

Base = declarative_base()
# Base.metadata.create_all(engine)
# DBSession = scoped_session(sessionmaker())
# engine = None

class TimeLogs(Base):
    __tablename__ = "timelogs"
    id = Column(Integer, primary_key=True)
    start_time = Column(String)
    end_time = Column(String)
    project_name = Column(String)
    date = Column(Date)
    h = Column(Float)
    user = Column(String, ForeignKey('master_db.user_ID'))


class Master_db(Base):
    __tablename__ = 'master_db'
    user_ID = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    timelogs = relationship("TimeLogs", backref="master_db")


class TimeStamps(Base):
    __tablename__ = "timestamps"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)

class Source:
    """
    This class represents Connection with Database

    Parameters
    ----------
    timelogs: List[str], optional
        The timelogs dict from text message.
        by default None
    database_name: str, optional
        by default sqlalchemy.db will be created in root directory.
    """
    # def __init__(self, messages: Dict[str, Any] = None, database_name: str = 'metabase',
    #                                                         timestamp: float = None):

    # def __init__(self,
    #              database_name: str = 'metabase'
    #              # timestamp: float = None
    #              ):

    def __init__(self, *args, database_name: str = 'metabase', **kwargs):
        logger = prefect.context.get("logger")
        # self.messages = messages
        self.database_name = database_name
        POSTGRES_URL = 'postgresql://{}:{}@{}:{}/{}'.format('postgres',        # user
                                                            'postgres',        # password
                                                            'database',        # host name
                                                            '5432',            # port
                                                            self.database_name # database)
                                                            )
        self.Base = declarative_base()
        self.DBSession = scoped_session(sessionmaker())
        self.engine = create_engine(POSTGRES_URL)
        self.DBSession.configure(bind=self.engine, autoflush=False, expire_on_commit=False)
        # self.Base.metadata.create_all(engine)
        # self.ts = timestamp


    @abstractmethod
    def insert_into(self):
        pass

    def insert_into_master_db(self, id, first_name, last_name, email):
        if not self.check_user_in_master_bd(id=id):
            self.DBSession.add(Master_db(user_ID=id, first_name=first_name,
                                    last_name=last_name, email=email))
            self.DBSession.commit()
            return True
        return False

    def delete_user(self, id):
        if self.check_user_in_master_bd(id=id):
            self.DBSession.query(Master_db).filter_by(user_ID=id).delete()
            self.DBSession.commit()
            return True
        return False

    def delete_timelog(self, user, delete_date):
        if self.check_timelog_in_day(user, delete_date):
            self.DBSession.query(TimeLogs).filter_by(user=user, date=delete_date).delete()
            self.DBSession.commit()
            return True
        return False


    def check_user_in_master_bd(self, id):
        user = self.DBSession.query(Master_db).filter_by(user_ID=id).first()
        if user:
            print("You are stupid!!!\n this User was created!!!")
            return True
        print("You create new User")
        return False

    # def add_timestamp_to_db(self):
    #     '''
    #         This function allow to add timestamp in flow task, for messages which
    #         are not a timelog
    #     '''
    #     DBSession.add(TimeStamps(timestamp=self.ts))
    #     DBSession.commit()


    # insert into from Slack
    # def insert_into(self):
    #     for message in self.messages:
    #         print("jeste w insert_into\n message: {}".format(message))
    #         if not self.check_duplicates(user=message['user'], start_time=message['start_time'],
    #                                                            date_time=message['date']):
    #             DBSession.add(TimeLogs(
    #                                    start_time=message['start_time'],
    #                                    end_time=message['end_time'],
    #                                    project_name=message['project_name'],
    #                                    user=message['user'],
    #                                    date=message['date'],
    #                                    h=message['h']
    #                                    ))
    #             DBSession.commit()
    #
    #             print("class Database - method: insert_into\nTHIS IS NOT A DUPLICATE!!!!")
    #         else:
    #             print("class Database - method: insert_into\nAWARE - THIS IS A DUPLICATE!!!!")


    def insert_bulk(self):
        self.DBSession.bulk_insert_mappings(
            TimeLogs,
            [
                timelog for timelog in self.messages
            ]
        )
        self.DBSession.commit()

        return True


    # def select_timestamps(self):
    #     table_record = []
    #     sql_select_query = DBSession.query(TimeStamps).all()
    #     for row in sql_select_query:
    #         table_record.append(row.timestamp)
    #     return table_record
    #
    # def select_last_timestamp_by_max(self):
    #     '''
    #         Select calculated last timestamp
    #     '''
    #     last_timestamp = DBSession.query(func.max(TimeStamps.timestamp)).scalar()
    #     return last_timestamp
    #
    # def select_last_timestamp(self):
    #     '''
    #         Select last timestamp by last record in table
    #     '''
    #     last_timestamp = DBSession.query(TimeStamps).order_by(TimeStamps.id.desc()).first()
    #     return last_timestamp.timestamp

    def select_master_db_user(self):
        result = []
        select_query = self.DBSession.query(Master_db).all()
        for row in select_query:
            print(f"{row.ID}, {row.name}")
            result.append(row.ID, row.name)
        return result

    def select_all_timelogs(self):
        table_record = []
        query = select(Master_db, Timelogs).join(Master_db.timelogs).all()
        for row in self.DBSession.execute(query):
            print(f"{row.Timelogs.start_time},\
                    {row.Timelogs.end_time},\
                    {row.Timelogs.project_name},\
                    {row.Timelogs.user},\
                    {row.Master_db.name}")
            table_record.append((row.Timelogs.start_time,
                                 row.Timelogs.end_time,
                                 row.Timelogs.project_name,
                                 row.Timelogs.user,
                                 row.Master_db.name))

        return table_record


    def check_duplicates(self, user, start_time, date_time):
        '''
            This function filter duplicates of timelog define
            User can not create timelog at the same start_time and date
        '''
        filter = self.DBSession.query(TimeLogs).filter_by(user=user, start_time=start_time, date=date_time).first()
        if filter:
            print("You are stupid!!!\n this Timelog was created by You")
            return True
        print("You create new Timelog")
        return False

    def check_timelog_in_day(self, user, date_time):
        filter = self.DBSession.query(TimeLogs).filter_by(user=user, date=date_time).first()
        if filter:
            return True
        return False
