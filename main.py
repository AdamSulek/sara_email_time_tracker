from fastapi import FastAPI, Body, Form, Request
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# import sys
#sys.path.insert(0,'..')
# sys.path.insert(0,'../..')
#sys.path.insert(0,'../../..')
# sys.path.append('/timelogs')

# Now you can import your module
# from database import TimeLogs
from timelogs.database import TimeLogs

templates = Jinja2Templates(directory="htmldirectory")

POSTGRES_URL = 'postgresql://{}:{}@{}:{}/{}'.format('postgres',        # user
                                                    'postgres',        # password
                                                    'database',        # host name
                                                    '5432',            # port
                                                    'metabase' # database)
                                                    )
engine = create_engine(POSTGRES_URL)
Base = declarative_base()
DBSession = scoped_session(sessionmaker())
DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)

Base.metadata.create_all(engine)

# class TimeLogs(Base):
#     __tablename__ = "timelogs"
#     id = Column(Integer, primary_key=True)
#     start_time = Column(String)
#     end_time = Column(String)
#     project_name = Column(String)
#     date = Column(Date)
#     h = Column(Float)
#     user = Column(String)
    # user = Column(String, ForeignKey('master_db.user_ID'))

app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
database = {}

class TimeLogs(BaseModel):
    id: int
    start_time: str = "8:00"
    end_time: str = "18:00"
    project_name: str = "wasting time :)"
    date: str = None
    h: float = None
    user: str = None

# timelogs_1 = TimeLogs(id=1)
# timelogs_2 = TimeLogs(id=2, date="21.12.2021", h="8.00", user="Adam")
# database[1] = timelogs_1
# database[2] = timelogs_2

@app.post("/add-timelogs/")
def add_new_timelogs(start_time: str = Form(...),
                     end_time: str = Form(...),
                     project_name: str = Form(...),
                     date: str = Form(...),
                     h: float = Form(...),
                     user: str = Form(...)):

    TimeLogs[start_time] = start_time
    TimeLogs[end_time] = end_time
    TimeLogs[project_name] = project_name
    TimeLogs[date] = date
    TimeLogs[h] = h
    TimeLogs[user] = user
    #return(start_time)
    return TimeLogs

@app.get("/timelogs/{timelog_id}")
def get_timelogs(timelog_id: int):
    for timelog_num, timelog in database.items():
        if timelog.id == timelog_id:
            return database[timelog_id]
    return {"Data": "not found"}




@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse( "home.html", {"request": request} )
    # return {"title": "Hello from anothe world and some changes and more or less\n bitch!"}




#updating
# @app.put("/timelogs/{timelog_id}")
# def update_timelogs(timelog_id: int, timelog: Item):
#     return {"item_name": item.name, "item_id": item_id}
