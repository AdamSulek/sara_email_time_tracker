from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData, Table, Column, Integer, String
from .message import Message
from typing import Any, Dict, List

Base = declarative_base()
DBSession = scoped_session(sessionmaker())
engine = None

class TimeLogs(Base):

    __tablename__ = "timelogs"
    id = Column(Integer, primary_key=True)
    timelog_name = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    project_name = Column(String)
    employee = Column(String)
    user = Column(String)


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
    def __init__(self, timelogs: List[str] = None, database_name: str = 'sqlite:///sqlalchemy.db'):
        self.timelogs = timelogs
        self.database_name = database_name
        engine = create_engine(self.database_name, echo=False)
        #DBSession.remove()
        DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
        #Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.user = self.timelogs[0]['user']
        self.start_time = self.timelogs[0]['start_time']
        #print("self.timelogs.project_name: {}".format(self.timelogs[0]['project_name']))

    def insert_into(self):
        if not self.check_duplicates():
            DBSession.add(TimeLogs(timelog_name=self.timelogs[0]['timelog_name'],
                                   start_time=self.timelogs[0]['start_time'],
                                   end_time=self.timelogs[0]['end_time'],
                                   project_name=self.timelogs[0]['project_name'],
                                   employee=self.timelogs[0]['employee'],
                                   user=self.timelogs[0]['user']
                                   ))
            DBSession.commit()
        #     print("THIS IS NOT A DUPLICATE!!!!")
        # else:
        #     print("AWARE - THIS IS A DUPLICATE!!!!")

    def insert_bulk(self):
        DBSession.bulk_insert_mappings(
            TimeLogs,
            [
                timelog for timelog in self.timelogs
            ]
        )
        DBSession.commit()

        return True

    def select_query(self):
        table_record = []
        sql_select_query = DBSession.query(TimeLogs).all()
        for row in sql_select_query:
            # print("event ID: {},\nevent_name: {},\n\
            #        start_time: {},\nend_time: {},\n\
            #        project_name: {},\nemployee: {}\n".format(row.id,
            #                                                  row.timelog_name,
            #                                                  row.start_time,
            #                                                  row.end_time,
            #                                                  row.project_name,
            #                                                  row.employee))
            table_record.append((row.id,
                                 row.timelog_name,
                                 row.start_time,
                                 row.end_time,
                                 row.project_name,
                                 row.employee,
                                 row.user))

        return table_record


    def check_duplicates(self):
        filter = DBSession.query(TimeLogs).filter_by(user=self.user, start_time=self.start_time).first()
        # print("user: {}\n start_time: {}\n filter: {}".format(self.user,
        #                                                       self.start_time,
        #                                                       filter))
        if filter:
            #print("DUPLICATE")
            return True
        #print("NOT DUPLICATE")
        return False
