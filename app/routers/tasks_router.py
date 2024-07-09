from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user_model import User
from app.schemas import task_schema
from app.utils.jwt_auth import get_current_user
import app.services.tasks_service as tasks_service

router = APIRouter(prefix="/tasks", tags=["tasks"], dependencies=[Depends(get_db)])


@router.get("/")
async def get_all_tasks_by_user(
    user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)
):
    """
    Retrieves all tasks associated with the current user.

    Parameters:
    - user (User): The current authenticated user.
    - db (Session): The database session.

    Returns:
    - List[task_schema.Task]: A list of tasks associated with the user.
    """
    try:
        return tasks_service.get_all_tasks_by_user(db=db, email=user.email)
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)


@router.post("/")
async def create_task(
    task: task_schema.TaskBase,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """
    Creates a new task for the current user.

    Parameters:
    - task (task_schema.TaskBase): The task data.
    - user (User): The current authenticated user.
    - db (Session): The database session.

    Returns:
    - task_schema.Task: The created task.
    """
    try:
        return tasks_service.create_task(db=db, task=task, email=user.email)
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)


@router.put("/")
async def update_task(
    task: task_schema.Task,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """
    Updates an existing task for the current user.

    Parameters:
    - task (task_schema.Task): The updated task data.
    - user (User): The current authenticated user.
    - db (Session): The database session.

    Returns:
    - task_schema.Task: The updated task.
    """
    try:
        return tasks_service.update_task(db=db, task=task, user_id=user.id)
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)


@router.delete("/{task_id}")
async def delete_task_by_id(
    task_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """
    Deletes a task by its ID for the current user.

    Parameters:
    - task_id (str): The ID of the task to delete.
    - user (User): The current authenticated user.
    - db (Session): The database session.

    Returns:
    - dict: A dictionary indicating the success of the deletion.
    """
    try:
        if not tasks_service.delete_task(db=db, task_id=task_id, user_id=user.id):
            return {"message": "Task deleted successfully"}
        return {"message": "Error while trying to delete task"}
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
