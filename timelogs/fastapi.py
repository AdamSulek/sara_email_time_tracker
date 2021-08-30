from sqlalchemy.orm import Session, scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData,\
                       Table, Column, Integer, String, Float, Date, ForeignKey
from typing import Any, Dict, List
from sqlalchemy import func
import logging
import prefect
import datetime
from .source import TimeLogs, MasterDb, Source


class Fastapi(Source):
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
    def __init__(self, *args, text_box: Dict[str, Any] = None, **kwargs):
        super().__init__(name="FastApi", *args, **kwargs)
        self.text_box = text_box


    def insert_into(self):

        for key, message in self.text_box.items():
            if key == "start_time":
                start_time = message
            if key == "end_time":
                end_time = message
            if key == "project_name":
                project_name = message
            if key == "user":
                user = message
            if key == "date":
                date = message
            if key == "h":
                h = message

        if not self.check_duplicates(user=user, start_time=start_time,
                                     date_time=date):
            self.DBSession.add(TimeLogs(
                                   start_time=start_time,
                                   end_time=end_time,
                                   project_name=project_name,
                                   user=user,
                                   date=date,
                                   h=h
                                   ))
            self.DBSession.commit()
            return True
        return False
