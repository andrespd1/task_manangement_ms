from sqlalchemy.orm import Session
from ..models import user_model
from ..schemas import user_schema
from app.utils import password_hashing


def create_user(db: Session, user: user_schema.UserCreate):
    """
    Creates a new user in the database.

    Parameters:
    - db (Session): The database session.
    - user (user_schema.UserCreate): The user data for creating a new user.

    Returns:
    - user_model.User: The created user.
    """
    hashed_password = password_hashing.get_password_hash(user.password)
    db_user = user_model.User(
        name=user.name, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    """
    Retrieves a user from the database by their email.

    Parameters:
    - db (Session): The database session.
    - email (str): The email of the user to be retrieved.

    Returns:
    - user_model.User: The user with the given email, or None if no user was found.
    """
    return db.query(user_model.User).filter(user_model.User.email == email).first()
