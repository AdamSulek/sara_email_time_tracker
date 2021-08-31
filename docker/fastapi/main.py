from fastapi import FastAPI, Body, Form, Request
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import date, datetime, timedelta
from timelogs.source import TimeLogs
from timelogs.slack import Slack
from timelogs.fastapi import Fastapi
from time import time

templates = Jinja2Templates(directory="html")

app = FastAPI()

# class Timelogs(BaseModel):
#     start_time: str = None
#     end_time: str = None
#     project_name: str = None
#     date: datetime = None
#     h: float = None
#     user: str = None


@app.get("/home/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse( "home.html", {"request": request} )


@app.post("/add-user/", response_class=HTMLResponse)
def add_new_user(request: Request,
                 id: str = Form(...),
                 first_name: str = Form(...),
                 last_name: str = Form(...),
                 email: str = Form(...)
                 ) -> HTMLResponse:
    db = Slack()
    new_user = db.insert_into_master_db(id=id, first_name=first_name,
                                          last_name=last_name, email=email)
    if not new_user:
        first_name = None
        last_name = None
    else:
        first_name = first_name
        lat_name = last_name

    return templates.TemplateResponse( "add-user.html", context={'request': request,
                                                                 'first_name': first_name,
                                                                 'last_name': last_name } )


@app.post("/delete-user/", response_class=HTMLResponse)
def delete_user(request: Request,
                 id: str = Form(...)
                 ) -> HTMLResponse:

    db = Slack()
    old_user = db.delete_user( id=id )
    if old_user:
        id = id
    else:
        id = None

    return templates.TemplateResponse( "delete-user.html",
                                       context={'request': request,
                                                'id': id } )


@app.post("/delete-timelogs/", response_class=HTMLResponse)
def delete_timelogs(request: Request,
                 user: str = Form(...),
                 delete_date: str = Form(...)
                 ) -> HTMLResponse:

    db = Slack()
    old_timelogs = db.delete_timelog(user, delete_date)

    if not old_timelogs:
        user = None
        delete_date = None
    else:
        user = user
        delete_date = delete_date

    return templates.TemplateResponse( "delete-timelogs.html",
                                        context={'request': request,
                                                 'user': user,
                                                 'delete_date': delete_date } )


@app.post("/add-timelogs/", response_class=HTMLResponse)
def add_new_timelogs(request: Request,
                     date_: date = Form(...),
                     start_time: str = Form(...),
                     end_time: str = Form(...),
                     project_name: str = Form(...),
                     # h: float = Form(...),
                     user: str = Form(...)
                     ) -> HTMLResponse:

    ts = time()
    api_post_request = {}
    api_post_request["start_time"] = start_time
    api_post_request["end_time"] = end_time
    api_post_request["project_name"] = project_name
    api_post_request["date"] = date_

    st_time_str = datetime.strptime(start_time, '%H:%M')
    en_time_str = datetime.strptime(end_time, '%H:%M')
    start_time_as_time = st_time_str.time()
    end_time_as_time = en_time_str.time()
    s_time = datetime.combine(date.today(), start_time_as_time)
    e_time = datetime.combine(date.today(), end_time_as_time)

    h = ((e_time - s_time).total_seconds()) / 3600

    api_post_request["h"] = h
    api_post_request["user"] = user # for now it is only my SLACK_ID, in future check list of available users
    api_post_request["ts"] = str(ts)

    db = Fastapi(text_box=api_post_request)
    new_timelog = db.insert_into()
    if new_timelog:
        h = h
    else:
        h = None

    return templates.TemplateResponse( "add-timelogs.html", context={'request': request,
                                                                     'h': h } )
