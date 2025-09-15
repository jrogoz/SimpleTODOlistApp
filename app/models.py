from sqlalchemy import Column, Integer, String, Enum
import enum

from app.database import Base


class StatusEnum(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"
    
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.TODO)