from sqlalchemy.orm import Session, scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select, create_engine, MetaData,\
                       Table, Column, Integer, String, Float, Date, ForeignKey
import pandas as pd
from .source import TimeLogs, Source
import os
from datetime import time, date, datetime, timedelta


class GoogleDrive(Source):
    # def __init__(self, path: str = None):
    def __init__(self, *args, path: str = None, **kwargs):
        super().__init__(name="GoogleDrive", *args, **kwargs)
        self.path = path
        self.df = None
        if os.path.isfile(self.path):
            self.df = pd.read_excel(self.path, header=0, index_col=False, keep_default_na=True)

    def create_headers(self):
        return self.df.columns


    def to_dict(self):
        whole_rows = []

        for date_ind, row in self.df.T.iteritems():
            #print("start time: {} - and type: {}".format(row['start'], type(row['start'])))
            #print("end time: {} - and type: {}".format(row['end'], type(row['end'])))
            single_row = {}

            if not isinstance(row['date'], datetime):
                date_ = datetime.strptime(row['date'], "%d-%m-%Y")
            if isinstance(row['date'], datetime):
                date_ = row['date']

            if isinstance(row['start'], time) and isinstance(row['end'], time):
                start_datetime = datetime.combine(date.today(), row['start'])
                end_datetime = datetime.combine(date.today(), row['end'])
                hh = ((end_datetime - start_datetime).total_seconds()) / 3600
                start_ = start_datetime.strftime('%H:%M')
                end_ = end_datetime.strftime('%H:%M')
                single_row['h'] = hh
                single_row['start_time'] = start_
                single_row['end_time'] = end_

            if not isinstance(row['start'], time) or not isinstance(row['end'], time):
                single_row['h'] = 0.0

            single_row = { "start_time": row['start'],
                           "end_time": row['end'],
                           "project_name": row['work_area'],
                           "user": row['contractor'],
                           "date": date_
                         }

            whole_rows.append(single_row)

            self.check_user_in_master_db_by_name(row['contractor'])

        return whole_rows

    def check_user_in_master_db_by_name(self, contractor):
        #session.query(Object).filter(Object.column.like('something%'))

        user = self.DBSession.query(Master_db).filter_by(last_name.like('contractor%')).first()
        if user:
            print("this User was created: {} !!!".format(user))
            return True
        print("You try create a User: {}".format(contractor))
        return False
