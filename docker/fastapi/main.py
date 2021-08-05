from fastapi import FastAPI

#from sqlalchemy.orm import Session
#
# from . import crud, models, schemas
# from .database import SessionLocal, engine
#
# from typing import List
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/")
def index():
    return {"title": "Hello from anothe world and some changes and more or less!"}
