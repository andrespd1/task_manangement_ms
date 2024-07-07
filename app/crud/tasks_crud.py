import datetime
from sqlalchemy import Session
from ..models import task_model
from ..schemas import task_schema


def create_task(db: Session, task: task_schema.Task):
    db_task = task_model.Task(
        title=task.title,
        description=task.description,
        created_date=datetime.now(),
        created_by=task.created_by,
        due_date=task.due_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_by_user(db: Session, user_id: str):
    return db.query(task_model.Task).filter(task_model.Task.created_by == user_id).all()


def delete_task_by_id(db: Session, task_id: str):
    deleted_task = (
        db.query(task_model.Task).filter(task_model.Task.id == task_id).delete()
    )
    db.commit()
    return deleted_task


def update_task_by_id(db: Session, task: task_schema.Task):
    task: task_model.Task = (
        db.query(task_model.Task)
        .filter(task_model.Task.id == task.id)
        .update(task.__dict__)
    )
    db.commit()
    db.refresh(task)
    return task
