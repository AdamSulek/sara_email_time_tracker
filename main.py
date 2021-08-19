from fastapi import FastAPI, Body, Form, Request
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import date, datetime, timedelta
from timelogs.database import TimeLogs, Database
import time

templates = Jinja2Templates(directory="htmldirectory")

# POSTGRES_URL = 'postgresql://{}:{}@{}:{}/{}'.format('postgres',        # user
#                                                     'postgres',        # password
#                                                     'database',        # host name
#                                                     '5432',            # port
#                                                     'metabase' # database)
#                                                     )
# engine = create_engine(POSTGRES_URL)
# Base = declarative_base()
# DBSession = scoped_session(sessionmaker())
# DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
# Base.metadata.create_all(engine)


app = FastAPI()

# def get_db():
#     DBSession = scoped_session(sessionmaker())
#     DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
#     Base.metadata.create_all(engine)
#     # db = SessionLocal()
#     try:
#         yield DBSession
#     finally:
#         DBSession.close()
        # db.close()


class Timelogs(BaseModel):
    start_time: str = None
    end_time: str = None
    project_name: str = None
    # date: str = None
    date: datetime = None
    h: float = None
    user: str = None

@app.post("/add-user/")
def add_new_user(id: str = Form(...),
                 user_name: str = Form(...)):
    db = Database()
    db.insert_into_master_db(id=id, user_name=user_name)
    return {"id": id, "user_time": user_name}

@app.post("/add-timelogs/")
def add_new_timelogs(start_time: str = Form(...),
                     end_time: str = Form(...),
                     project_name: str = Form(...),
                     #date: str = Form(...),
                     h: float = Form(...)
                     #user: str = Form(...)
                     ):

    today_str = datetime.today().strftime("%d.%m.%Y")
    ts = time.time()
    api_post_request = {}
    api_post_request["start_time"] = start_time
    api_post_request["end_time"] = end_time
    api_post_request["project_name"] = project_name
    api_post_request["date"] = datetime.strptime(today_str, "%d.%m.%Y")
    api_post_request["h"] = h
    api_post_request["user"] = 'U02A69XJ49K' # for now it is only my SLACK_ID, in future check list of available users
    api_post_request["ts"] = str(ts)

    # result = Timelogs(**api_post_request)
    #dd = datetime.strptime(today_str, "%d.%m.%Y")

    print("========================= {} =======================".format(api_post_request))
    message = {
        "start_time": start_time,
        "end_time": end_time,
        "project_name": project_name,
        "h": h,
        "user": 'U02A69XJ49K',
        "date": datetime.strptime(today_str, "%d.%m.%Y"),
        "ts": str(ts)
    }

    db = Database(messages=api_post_request)
    db.insert_from_api()
    # db.insert_into()

    return api_post_request


@app.get("/timelogs/{timelog_id}")
def get_timelogs(timelog_id: int):
    for timelog_num, timelog in database.items():
        if timelog.id == timelog_id:
            return database[timelog_id]
    return {"Data": "not found"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse( "home.html", {"request": request} )


#updating
# @app.put("/timelogs/{timelog_id}")
# def update_timelogs(timelog_id: int, timelog: Item):
#     return {"item_name": item.name, "item_id": item_id}
