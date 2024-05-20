from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.engine.db_engine import DBStorage
from models.task_model import Task
from models.user_model import User
from web_flask.admin_management import admin_user

db_storage = DBStorage()


class CreateTask(Resource):
    @jwt_required()  # Apply JWT protection to the endpoint
    def post(self):
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        user = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user:
            return {'message': 'User not found'}, 404

        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract expected fields for creating a task
        task_title = data.get('task_title')
        task_description = data.get('task_description')
        task_group = data.get('task_group')
        # Add more fields as needed (e.g., due_date, priority)

        # Validate required fields
        if not task_title:
            return {'message': 'Missing required field: task_title'}, 400

        # Create a new task object
        new_task = Task(
            task_title=task_title,
            task_description=task_description,
            created_by = user.email,
            updated_by = user.email,
            moved_by = user.email,
            task_group = task_group
        )

        # Additional logic for setting task group, assignee, etc. (optional)

        # Add the task to the database
        db_storage.add(new_task)
        db_storage.commit()

        return {'message': 'Task created successfully'}, 201


class GetTask(Resource):
    @jwt_required()
    def get(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400
        
        task_group = data.get('task_group')
        
        tasks = db_storage.get_specified_objects_by_attribute(Task, 'task_group', task_group)

        # Check if task exists
        if not tasks:
            return {'message': 'Task not found'}, 404
        
        task_data_list = []

        for task in tasks:

            # Prepare response data (dictionary)
            task_data = {
                'task_id': task.task_id,
                'task_title': task.task_title,
                'task_description': task.task_description,
                'task_group': task.task_group,
                'created_by': task.created_by,
                'updated_by': task.updated_by,
                'moved_by': task.moved_by,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat()
            }
            task_data_list.append(task_data)

        return jsonify(task_data_list)


class UpdateTask(Resource):
    @jwt_required()
    def patch(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400
        
        task_id = data.get('task_id')

        # Get the task object by ID
        task = db_storage.get_object_by_attribute(Task, task_id=task_id)

        # Check if task exists
        if not task:
            return {'message': 'Task not found'}, 404

        # Extract fields for update (optional)
        # You can choose to allow updating specific fields or all
        task_title = data.get('task_title')
        task_description = data.get('task_description')
        task_group = data.get('task_group')
        # Add more fields for update as needed (e.g., due_date, priority)

        user_id = get_jwt_identity()

        user = db_storage.get_object_by_attribute(User, user_id=user_id)

        # Update task attributes (consider validation if needed)
        if task_title:
            task.task_title = task_title
        if task_description:
            task.task_description = task_description
        if task_group:
            task.task_group = task_group
            task.moved_by = user.email

        # Update the 'updated_by' field with the current user
        task.updated_by = user.email

        # Additional logic for updating related entities (optional)

        # Update the task in the database
        db_storage.add(task)
        db_storage.commit()

        return {'message': 'Task updated successfully'}, 200


class DeleteTask(Resource):
    @jwt_required()
    @admin_user
    def delete(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400
        
        task_id = data.get('task_id')

        # Get the task object by ID
        task = db_storage.get_object_by_attribute(Task, task_id=task_id)

        # Check if task exists
        if not task:
            return {'message': 'Task not found'}, 404

        # Delete the task from the database
        db_storage.delete_object_by_attribute(Task, task_id=task_id)
        db_storage.commit()

        return {'message': 'Task deleted successfully'}, 200
