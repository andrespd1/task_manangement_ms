from typing import Annotated
from app.utils.jwt_auth import Token
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
import app.services.users_service as users_service
from app.schemas.user_schema import UserCreate
from app.dependencies import get_db
from sqlalchemy.orm import Session

# Define the router for user-related endpoints
router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_db)])


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = router.dependencies[0],
) -> Token:
    """
    Endpoint for user login. Validates user credentials and returns a JWT token.

    Parameters:
    - form_data (OAuth2PasswordRequestForm): The form data containing username and password.
    - db (Session): The database session.

    Returns:
    - Token: A JWT token if login is successful.

    Raises:
    - HTTPException: If login fails with appropriate status code and message.
    """
    try:
        return users_service.login_user(db, form_data.username, form_data.password)
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)


@router.post("/signup")
async def sign_up(user: UserCreate, db: Session = router.dependencies[0]):
    """
    Endpoint for user registration. Registers a new user and returns the user data along with a JWT token.

    Parameters:
    - user (UserCreate): The user data for registration.
    - db (Session): The database session.

    Returns:
    - dict: A dictionary containing the created user and a JWT token.

    Raises:
    - HTTPException: If registration fails with appropriate status code and message.
    - HTTPException(500): If an unexpected error occurs.
    """
    try:
        return users_service.register_user(db, user)
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception as e:
        raise HTTPException(500, "An error has occurred! Please try again later.")
