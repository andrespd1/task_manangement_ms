import uuid
from sqlalchemy import UUID, Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from ..dependencies import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    created_date = Column(Date)
    user_id = Column(UUID, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="tasks")
    due_date = Column(Date)
