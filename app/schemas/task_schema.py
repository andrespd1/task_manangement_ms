from datetime import date
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    due_date: date
    created_by: str


class Task(TaskBase):
    id: str

    class Config:
        orm_mode = True
