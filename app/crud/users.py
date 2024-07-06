from sqlalchemy import Session
from ..models import user_model
from ..schemas import user_schema
from app.utils import password_hashing


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = password_hashing.get_password_hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
