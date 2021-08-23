from sqlalchemy.orm import Session, scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData,\
                       Table, Column, Integer, String, Float, Date, ForeignKey
import pandas as pd
from .source import TimeLogs, Database
import os

# Base = declarative_base()
# DBSession = scoped_session(sessionmaker())
# engine = None

class GoogleDrive(Source):
    # def __init__(self, *args, path: str = None, **kwargs):
    def __init__(self, path: str = None):
        self.path = path
        self.df = None
        if os.path.isfile(self.path):
            self.df = self.from_file()

        # self.df = pd.read_excel(self.path,
        #             # sheetname=0,
        #             header=0,
        #             index_col=False,
        #             keep_default_na=True
        #             )

        # POSTGRES_URL = 'postgresql://{}:{}@{}:{}/{}'.format('postgres',        # user
        #                                                     'postgres',        # password
        #                                                     'database',        # host name
        #                                                     '5432',            # port
        #                                                     'metabase' # database)
        #                                                     )
        # engine = create_engine(POSTGRES_URL)
        # DBSession.remove()
        # DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
        # Base.metadata.create_all(engine)
        # self.timelogs = []


    def from_file(self):
        df = pd.read_excel(self.path,
                    # sheetname=0,
                    header=0,
                    index_col=False,
                    keep_default_na=True
                    )
        return df


    def create_headers(self):
        return self.df.columns


    def insert_bulk(self):
        DBSession.bulk_insert_mappings(
            TimeLogs,
            [
                timelog for timelog in self.df
            ]
        )
        DBSession.commit()

        return True
