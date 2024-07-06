from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..dependencies import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="created_by")
