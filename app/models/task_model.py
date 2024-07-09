import uuid
from sqlalchemy import UUID, Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from ..dependencies import Base


class Task(Base):
    """
    SQLAlchemy model for the Task.

    Attributes:
    - id (UUID): The unique identifier of the task.
    - title (str): The title of the task.
    - description (str): The description of the task.
    - created_date (Date): The date when the task was created.
    - user_id (UUID): The ID of the user who created the task.
    - created_by (relationship): The relationship to the user who created the task.
    - due_date (Date): The due date of the task.
    """

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    created_date = Column(Date)
    user_id = Column(UUID, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="tasks")
    due_date = Column(Date)
