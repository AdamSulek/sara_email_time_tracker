from sqlalchemy.orm import Session, scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData,\
                       Table, Column, Integer, String, Float, Date, ForeignKey
import pandas as pd
from .source import TimeLogs, Source
import os


class GoogleDrive(Source):
    #def __init__(self, path: str = None):
    def __init__(self, *args, path: str = None, **kwargs):
        super().__init__(name="GoogleDrive", *args, **kwargs)
        self.path = path
        self.df = None
        if os.path.isfile(self.path):
            self.df = self.to_df()

    def to_df(self):
        df = pd.read_excel(self.path,
                    header=0,
                    index_col=False,
                    keep_default_na=True
                    )
        return df


    def create_headers(self):
        return self.df.columns


    def insert_bulk(self):
        self.DBSession.bulk_insert_mappings(
            TimeLogs,
            [
                timelog for timelog in self.df
            ]
        )
        self.DBSession.commit()

        return True
