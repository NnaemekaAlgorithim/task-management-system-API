from uuid import uuid4
from sqlalchemy import Column, String, PrimaryKeyConstraint
from models.base_model import Base
from models.base_model import BaseModel


class TaskGroup(BaseModel, Base):
    """Represents a group of tasks.

    Attributes:
        task_group_id (Integer): The primary key for the task group.
        task_group_title (String): The title of the task group (required, unique).
    """

    __tablename__ = "task_group"

    task_group_id = Column(String(60), primary_key=True)
    task_group_title = Column(String(255), nullable=False, unique=True)

    __table_args__ = (PrimaryKeyConstraint('task_group_id'),)

    def __init__(self, *args, **kwargs):
        """Initialize a new User."""
        super().__init__(*args, **kwargs)
        self.task_group_id = uuid4().hex
