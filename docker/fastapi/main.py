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

templates = Jinja2Templates(directory="html")

app = FastAPI()

class Timelogs(BaseModel):
    start_time: str = None
    end_time: str = None
    project_name: str = None
    # date: str = None
    date: datetime = None
    h: float = None
    user: str = None


@app.get("/home/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse( "home.html", {"request": request} )

# @app.post("/add-user/", response_class=HTMLResponse)
# def add_new_user(request: Request):
#     return templates.TemplateResponse( "add-user.html", {"request": request} )
#
#
# @app.post("/add-timelogs/", response_class=HTMLResponse)
# def add_new_user(request: Request):
#     return templates.TemplateResponse( "add-timelogs.html", {"request": request} )


@app.post("/add-user/")
def add_new_user(id: str = Form(...),
                 first_name: str = Form(...),
                 last_name: str = Form(...),
                 email: str = Form(...)
                 ):
    db = Database()
    db.insert_into_master_db(id=id, first_name=first_name,
                             last_name=last_name, email=email)

    return {"first_name": first_name, "last_name": last_name}


@app.post("/add-timelogs/")
def add_new_timelogs(start_time: str = Form(...),
                     end_time: str = Form(...),
                     project_name: str = Form(...),
                     #date: str = Form(...),
                     h: float = Form(...),
                     user: str = Form(...)
                     ):

    today_str = datetime.today().strftime("%d.%m.%Y")
    ts = time.time()
    api_post_request = {}
    api_post_request["start_time"] = start_time
    api_post_request["end_time"] = end_time
    api_post_request["project_name"] = project_name
    api_post_request["date"] = datetime.strptime(today_str, "%d.%m.%Y")
    api_post_request["h"] = h
    api_post_request["user"] = user # for now it is only my SLACK_ID, in future check list of available users
    api_post_request["ts"] = str(ts)


    # message = {
    #     "start_time": start_time,
    #     "end_time": end_time,
    #     "project_name": project_name,
    #     "h": h,
    #     "user": user,
    #     "date": datetime.strptime(today_str, "%d.%m.%Y"),
    #     "ts": str(ts)
    # }

    db = Database(messages=api_post_request)
    db.insert_from_api()

    return api_post_request
