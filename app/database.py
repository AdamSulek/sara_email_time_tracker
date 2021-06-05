from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData, Table, Column, Integer, String
from .message import Message
#from .table import events_table
from typing import Any, Dict, List

import time

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

    def __init__(self, timelogs: List[str] = None, database_name: str = 'sqlite:///sqlalchemy.db'):
        self.timelogs = timelogs
        self.database_name = database_name
        engine = create_engine(self.database_name, echo=False)
        DBSession.remove()
        DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


    def insert_bulk(self):
        #self.init_sqlalchemy()
        t0 = time.time()
        DBSession.bulk_insert_mappings(
            TimeLogs,
            [
                timelog for timelog in self.timelogs
            ]
        )
        DBSession.commit()
        print(
            "SQLAlchemy ORM bulk_save_objects(): Total time for " +
            " records " + str(time.time() - t0) + " secs" + '\n')

    def select_query(self):
        sql_select_query = DBSession.query(TimeLogs).all()
        for row in sql_select_query:
            print("event ID: {},\nevent_name: {},\n\
                   start_time: {},\nend_time: {},\n\
                   project_name: {},\nemployee: {}\n".format(row.id,
                                                              row.timelog_name,
                                                              row.start_time,
                                                              row.end_time,
                                                              row.project_name,
                                                              row.employee))

        #return sql_select_query
