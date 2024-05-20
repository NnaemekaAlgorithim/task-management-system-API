from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.base_model import Base


class Task(BaseModel, Base):
    """Represents a task within a task group.

    Attributes:
        task_id (Integer): The primary key for the task. Auto-increments.
        task_title (String): The title of the task (required, max 255 characters).
        task_description (String): A description of the task (optional, max 1024 characters).
        created_by (String): The email address of the user who created the task.
        updated_by (String): The email address of the user who last updated the task.
        moved_by (String): The email address of the user who last moved the task.
        task_group_id (Integer): Foreign key referencing the id column of the task_group table. 
                                 (Required, a task must belong to a task group).
        task_group (TaskGroup): Relationship to the TaskGroup model, allowing access to the 
                                 associated task group for a task object.
    """

    __tablename__ = "task"

    task_id = Column(String(60), primary_key=True)
    task_title = Column(String(255), nullable=False)
    task_description = Column(String(1024))
    created_by = Column(String(128))  # Email of user who created the task
    updated_by = Column(String(128))  # Email of user who last updated the task
    moved_by = Column(String(128))  # Email of user who last moved the task
    task_group = Column(String(255), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new User."""
        super().__init__(*args, **kwargs)
        self.task_id = uuid4().hex
