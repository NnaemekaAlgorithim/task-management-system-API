#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from pymysql import connect, cursors
#from models.user_model import User
#from models.task_group_model import TaskGroup
#from models.task_model import Task


class DBStorage:
    """Represents a database storage engine with generic CRUD methods.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
        __model_map (dict): A dictionary mapping model classes to their table names.
    """

    __engine = None
    __session = None
#    __model_map = {}


    def __init__(self):
        """Initialize a new DBStorage instance."""
        # Connect to database using environment variables
        self.__engine = create_engine(
            "mysql+pymysql://{}:{}@{}:{}/{}".format(
                getenv("MYSQL_USER_API"),
                getenv("MYSQL_PWD"),
                getenv("MYSQL_HOST"),
                getenv("MYSQL_PORT", "3306"),
                getenv("MYSQL_DB")
            )
        )
        self.__Session = sessionmaker(bind=self.__engine, autoflush=True)
        self.__session = scoped_session(self.__Session)

        # Register model classes (replace with your actual model classes)
#        self.__model_map = {User: "users"}
#        self.__model_map = {TaskGroup: "taskGroup"}
#        self.__model_map = {Task: "task"}

    def get_object_by_attribute(self, model, **kwargs):
        """Retrieves an object by its attributes from the database.

        Args:
            model: The model class to query.
            kwargs: A dictionary of attribute names and values for filtering.

        Returns:
            The first object matching the criteria or None if not found.
        """

        # Access session using the public method
        session = self.session()  # Call the session method
        obj = session.query(model).filter_by(**kwargs).first()
        session.close()  # Close the session explicitly
        return obj
    
    def get_all_objects(self, model):
        """Retrieves all objects from a database table.

        Args:
            model: The model class representing the table.

        Returns:
            A list of all objects in the table.
        """

        # Access session using the public method
        session = self.session()  # Call the session method
        objects = session.query(model).all()
        session.close()  # Close the session explicitly
        return objects
    
    def get_specified_objects_by_attribute(self, model, attribute_name, attribute_value):
        """Retrieves all objects from a database table matching a specific attribute.

        Args:
            model: The model class representing the table.
            attribute_name: The name of the attribute to filter by.
            attribute_value: The value to match in the specified attribute.

        Returns:
            A list of all objects matching the filter criteria.
        """

        # Access session using the public method
        session = self.session()  # Call the session method

        # Apply filter based on attribute
        objects = session.query(model).filter(getattr(model, attribute_name) == attribute_value).all()

        session.close()  # Close the session explicitly
        return objects

    def delete_object_by_attribute(self, model, **kwargs):
        """Deletes an object by its attributes from the database.

        Args:
            model: The model class to query.
            kwargs: A dictionary of attribute names and values for filtering.

        Returns:
            True if the object was deleted, False if not found.
        """
        session = self.session()  # Call the session method
        obj = session.query(model).filter_by(**kwargs).first()
        if obj:
            session.delete(obj)
            session.commit()
            session.close()  # Close the session explicitly
            return True
        session.close()  # Close the session explicitly even if object is not found
        return False
    
    def session(self):
        """Returns the current session."""
        return self.__session
    
    def add(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)
    
    def commit(self):
        """commit changes to database."""
        self.__session.commit()
