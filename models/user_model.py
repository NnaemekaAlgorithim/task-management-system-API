#!/usr/bin/python3
"""Defines the User class."""
from uuid import uuid4
from sqlalchemy import Boolean, Column
from sqlalchemy import String
from models.base_model import BaseModel
from models.base_model import Base

class User(BaseModel, Base):
    """Represents a user for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table user.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store users.
        first_name (sqlalchemy String): The user's first name.
        last_name (sqlalchemy String): The user's last name.
        email (sqlalchemy String): The user's email address.
        confirmed (sqlalchemy boolean): checks if user is confirmed by admin.
        password (sqlalchemy String): The user's password.
    """
    __tablename__ = "user"
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    user_id = Column(String(60), primary_key=True)
    confirmed = Column(Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new User."""
        super().__init__(*args, **kwargs)
        self.user_id = uuid4().hex
