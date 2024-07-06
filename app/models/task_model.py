from sqlalchemy import Column, Date, String
from sqlalchemy.orm import relationship
from ..dependencies import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_date = Column(Date)
    created_by = relationship("User", back_populates="tasks")
    due_date = Column(Date)
