from datetime import date
from pydantic import BaseModel


class TaskBase(BaseModel):
    """
    Base schema for a task.

    Attributes:
    - title (str): The title of the task.
    - description (str): The description of the task.
    - due_date (date): The due date of the task.
    """

    title: str
    description: str
    due_date: date


class Task(TaskBase):
    """
    Schema for a task with an ID.

    Attributes:
    - id (str): The unique identifier of the task.
    """

    id: str
    created_by: str

    class Config:
        orm_mode = True
