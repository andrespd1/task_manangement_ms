import datetime
from sqlalchemy.orm import Session
from ..models import task_model
from ..schemas import task_schema


def create_task(db: Session, task: task_schema.TaskBase, user_id: str):
    """
    Creates a new task in the database.

    Parameters:
    - db (Session): The database session.
    - task (task_schema.Task): The task data for creating a new task.

    Returns:
    - task_model.Task: The created task.
    """
    db_task = task_model.Task(
        title=task.title,
        description=task.description,
        created_date=datetime.datetime.now(),
        user_id=user_id,
        due_date=task.due_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_by_user(db: Session, user_id: str):
    """
    Retrieves all tasks created by a specific user.

    Parameters:
    - db (Session): The database session.
    - user_id (str): The ID of the user whose tasks are to be retrieved.

    Returns:
    - List[task_model.Task]: A list of tasks created by the user.
    """
    return db.query(task_model.Task).filter(task_model.Task.user_id == user_id).all()


def get_task_by_id(db: Session, task_id: str):
    """
    Retrieves a task by its ID.

    Parameters:
    - db (Session): The database session.
    - task_id (str): The ID of the task to be retrieved.

    Returns:
    - task_model.Task: The task with the specified ID, or None if not found.
    """
    return db.query(task_model.Task).filter(task_model.Task.id == task_id).first()


def delete_task_by_id(db: Session, task_id: str):
    """
    Deletes a task from the database by its ID.

    Parameters:
    - db (Session): The database session.
    - task_id (str): The ID of the task to be deleted.

    Returns:
    - int: The number of rows affected (should be 1 if the task was deleted).
    """
    deleted_task = (
        db.query(task_model.Task).filter(task_model.Task.id == task_id).delete()
    )
    db.commit()
    return deleted_task


def update_task_by_id(db: Session, task: task_schema.Task):
    """
    Updates a task in the database by its ID.

    Parameters:
    - db (Session): The database session.
    - task (task_schema.Task): The updated task data.

    Returns:
    - task_model.Task: The updated task.
    """
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task.id).first()
    if db_task:
        for key, value in task.__dict__.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task
