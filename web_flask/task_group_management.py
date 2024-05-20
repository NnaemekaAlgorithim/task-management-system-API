from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.engine.db_engine import DBStorage
from models.task_group_model import TaskGroup
from web_flask.admin_management import admin_user
db_storage = DBStorage()

class CreateTaskGroup(Resource):
    @jwt_required()  # Apply JWT protection to the endpoint
    @admin_user
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract only the expected field - task_group_title
        task_group_title = data.get('task_group_title')

        if not task_group_title:
            return {'message': 'Missing required field: task_group_title'}, 400

        # Create new task group
        task_group = TaskGroup(task_group_title=task_group_title)  # Replace with your model's field name

        # Check for additional fields you might want to include

        db_storage.add(task_group)
        db_storage.commit()  # Commit changes to the database

        return {'message': 'Task Group created successfully'}, 201


class UpdateTaskGroup(Resource):
    @jwt_required()  # Apply JWT protection
    @admin_user
    def patch(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract only allowed fields for update (e.g., title)
        task_group_title = data.get('task_group_title')  # Replace with allowed fields
        task_group_id = data.get('task_group_id')

        # Check if task_group_id exists
        task_group = db_storage.get_object_by_attribute(TaskGroup, task_group_id=task_group_id)
        if not task_group:
            return {'message': 'Task group not found'}, 404

        # Update task group object with allowed fields
        task_group.task_group_title = task_group_title  # Update allowed fields

        db_storage.add(task_group)  # Update the object in the database
        db_storage.commit()

        return {'message': 'Task Group updated successfully'}, 200


class GetAllTaskGroups(Resource):
    @jwt_required()  # Apply JWT protection
    @admin_user
    def get(self):
        # Get all task groups
        task_groups = db_storage.get_all_objects(TaskGroup)

        # Prepare response data (list of dictionaries)
        task_group_data = []
        for task_group in task_groups:
            data = {
                'task_group_id': task_group.task_group_id,  # Assuming 'id' is the primary key
                'task_group_title': task_group.task_group_title,
                'created_at': task_group.created_at.isoformat(),  # Convert datetime to ISO format
                'updated_at': task_group.updated_at.isoformat(),
            }
            task_group_data.append(data)

        return jsonify(task_group_data)

class DeleteTaskGroup(Resource):
    @jwt_required()  # Apply JWT protection
    @admin_user
    def delete(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400
        
        task_group_id = data.get('task_group_id')

        # Check if task_group_id exists
        task_group = db_storage.get_object_by_attribute(TaskGroup, task_group_id=task_group_id)
        if not task_group:
            return {'message': 'Task group not found'}, 404

        # Delete task group
        db_storage.delete_object_by_attribute(TaskGroup, task_group_id=task_group_id)

        return {'message': 'Task Group deleted successfully'}, 200
