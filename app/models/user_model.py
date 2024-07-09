from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship
from ..dependencies import Base
import uuid


class User(Base):
    """
    SQLAlchemy model for the User.

    Attributes:
    - id (UUID): The unique identifier of the user.
    - name (str): The name of the user.
    - email (str): The email address of the user, which must be unique.
    - hashed_password (str): The hashed password of the user.
    - tasks (relationship): The relationship to the tasks created by the user.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="created_by")
