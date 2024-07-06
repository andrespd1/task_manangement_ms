from datetime import date
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str


class Task(TaskBase):
    id: str

    class Config:
        orm_mode = True
