from datetime import timedelta
from fastapi import Depends, HTTPException
from app.utils.jwt_auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, Token
from app.utils.password_hashing import verify_password
from app.models.user_model import User
import app.crud.users_crud as users_crud
from app.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session


def get_user(db: Session, email: str):
    """
    Retrieves a user based on the provided email.

    Parameters:
    - db (Session): The database session.
    - email (str): The email of the user to be retrieved.

    Returns:
    - User: The user associated with the given email.

    Raises:
    - HTTPException(400): If the given email doesn't exist.
    """
    user: User = users_crud.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(400, "The given email doesn't exist")
    return user


def generate_token(email: str):
    """
    Generates a JWT token for the given user ID and email.

    Parameters:
    - id (UUID): The ID of the user.
    - email (str): The email of the user.

    Returns:
    - Token: A JWT token with the user's ID and email.
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="Bearer")


def login_user(db: Session, email: str, password: str):
    """
    Authenticates a user and generates a JWT token if the credentials are valid.

    Parameters:
    - db (Session): The database session.
    - email (str): The email of the user attempting to log in.
    - password (str): The password of the user attempting to log in.

    Returns:
    - Token: A JWT token if the login is successful.

    Raises:
    - HTTPException(401): If the email or password is invalid.
    """
    user: User = get_user(db=db, email=email)
    if not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Email or password is invalid")
    return generate_token(user.email)


def register_user(db: Session, user: UserCreate):
    """
    Registers a new user and generates a JWT token.

    Parameters:
    - db (Session): The database session.
    - user (UserCreate): The user data for registration.

    Returns:
    - dict: A dictionary containing the created user and a JWT token.

    Raises:
    - HTTPException(400): If the email is already in use, the name is empty, or the passwords do not match.
    """
    user.name = user.name.strip()
    if users_crud.get_user_by_email(db=db, email=user.email) != None:
        raise HTTPException(400, "The email is already in use")
    if len(user.name) == 0:
        raise HTTPException(400, "The name can't be empty")
    if user.password != user.repeat_password:
        raise HTTPException(400, "The passwords doesn't match")
    return {
        "user": users_crud.create_user(db=db, user=user),
        "token": generate_token(user.email),
    }
