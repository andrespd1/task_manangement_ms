from datetime import timedelta
from fastapi import Depends, HTTPException
from app.utils.jwt_auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, Token
from app.utils.password_hashing import verify_password
from app.models.user_model import User
import app.crud.users_crud as users_crud
from app.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session


def login_user(db: Session, email: str, password: str):
    user: User = users_crud.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(400, "The given email doesn't exist")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Email or password is invalid")
    return generate_token(user.email)


def register_user(db: Session, user: UserCreate):
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


def generate_token(email: str):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
