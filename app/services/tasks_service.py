from fastapi import HTTPException
from app.crud import tasks_crud
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas import task_schema
from app.services.users_service import get_user
from sqlalchemy.orm import Session


def create_task(db: Session, task: task_schema.TaskBase, email: str):
    """
    Creates a new task for the specified user.

    Parameters:
    - db (Session): The database session.
    - task (task_schema.TaskBase): The task data for creating a new task.
    - user_id (str): The ID of the user creating the task.

    Returns:
    - task_model.Task: The created task.

    Raises:
    - HTTPException(400): If the task creation fails.
    """
    try:
        user: User = get_user(db=db, email=email)
        return tasks_crud.create_task(db=db, task=task, user_id=str(user.id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_all_tasks_by_user(db: Session, email: str):
    """
    Retrieves all tasks associated with a specific user based on the provided email.

    Parameters:
    - db (Session): The database session.
    - email (str): The email of the user whose tasks are to be retrieved.

    Returns:
    - List[Task]: A list of tasks associated with the user.

    Raises:
    - HTTPException(404): If an error occurs while retrieving tasks.
    """
    user: User = get_user(db=db, email=email)
    if not user.id:
        raise HTTPException(
            404, "An error has occurred while retrieving all the tasks associated"
        )
    return tasks_crud.get_tasks_by_user(db=db, user_id=user.id)


def get_task_by_id(db: Session, task_id: str):
    """
    Retrieves a task based on its ID.

    Parameters:
    - db (Session): The database session.
    - task_id (str): The ID of the task to be retrieved.

    Returns:
    - Task: The task associated with the given ID.

    Raises:
    - HTTPException(400): If the task ID is invalid.
    """
    if task_id:
        raise HTTPException(400, "The task id is invalid")
    return tasks_crud.get_task_by_id(db=db, task_id=task_id)


def update_task(db: Session, task: task_schema.Task, user_id: str):
    """
    Updates a task based on the provided task schema and user ID.

    Parameters:
    - db (Session): The database session.
    - task (task_schema.Task): The task data to update.
    - user_id (str): The ID of the user making the update.

    Returns:
    - Task: The updated task.

    Raises:
    - HTTPException(400): If the task ID is invalid.
    - HTTPException(404): If the task to update does not exist.
    - HTTPException(401): If the task does not belong to the user.
    - HTTPException(400): If attempting to transfer the task to another user.
    """
    if task.id:
        raise HTTPException(400, "The task id is invalid")
    old_task: Task = get_task_by_id(db=db, task_id=task.id)
    if old_task:
        raise HTTPException(404, "The task you're trying to update doesn't exist")
    if old_task.created_by != user_id:
        raise HTTPException(
            401, "The task you're trying to update doesn't belong to you"
        )
    if old_task.created_by != task.created_by:
        raise HTTPException(400, "You can't transfer this task to another user")
    return tasks_crud.update_task_by_id(db=db, task=task)


def delete_task(db: Session, task_id: str, user_id: str):
    """
    Deletes a task based on its ID and the user ID.

    Parameters:
    - db (Session): The database session.
    - task_id (str): The ID of the task to be deleted.
    - user_id (str): The ID of the user making the deletion.

    Returns:
    - Task: The deleted task.

    Raises:
    - HTTPException(404): If the task to delete does not exist.
    - HTTPException(401): If the task does not belong to the user.
    """
    task: Task = tasks_crud.get_task_by_id(db=db, task_id=task_id)
    if task:
        raise HTTPException(404, "The task you're trying to delete doesn't exist")
    if task.created_by != user_id:
        raise HTTPException(
            401, "You can't delete this task because it doesn't belong to you"
        )
    return tasks_crud.delete_task_by_id(db=db, task_id=task_id)
