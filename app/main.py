from typing import Union

from fastapi import FastAPI

from app.dependencies import SessionLocal, engine
from app.models import user_model

app = FastAPI()

user_model.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
