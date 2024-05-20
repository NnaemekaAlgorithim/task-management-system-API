from flask import request, jsonify, session
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from models.engine.db_engine import DBStorage
from models.user_model import User
from flask_bcrypt import Bcrypt
from web_flask.admin_management import admin_user
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker

# Initialize Bcrypt instance (assuming it's configured in app.py)
bcrypt = Bcrypt()

db_storage = DBStorage()

class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user data from request
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        # Add additional required fields here

        # Check if user already exists
        existing_user = db_storage.get_object_by_attribute(User, email=email)
        if existing_user:
            return {'message': 'Email already exists, please login'}, 400

        # Hash the password before saving
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user
        user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db_storage.add(user)
        db_storage.commit()  # Commit changes to the database

        # Generate JWT token
        access_token = create_access_token(identity=email)
        return {'message': 'Registration successful', 'access_token': access_token}, 201

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user data from request
        email = data.get('email')
        password = data.get('password')

        # Check if user exists
        user = db_storage.get_object_by_attribute(User, email=email)
        if not user:
            return {'message': 'Invalid email or password'}, 401

        # Verify password hash
        if not bcrypt.check_password_hash(user.password, password):
            return {'message': 'Invalid email or password'}, 401

        # Login successful, generate access token
        access_token = create_access_token(identity=user.user_id)  # Use user ID for identity

        return {'message': 'Login successful', 'access_token': access_token}, 200

class UserProfile(Resource):
    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def get(self):
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        # Retrieve the user from the database using the user_id
        user = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user:
            return {'message': 'User not found'}, 404

        # Return the user's profile details, excluding the password
        user_profile = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }

        return jsonify(user_profile)

class UpdateUser(Resource):
    @jwt_required()
    def patch(self):
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID
        print(current_user_id)
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Ensure at least one data field is provided
        if not any(field in data for field in ['first_name', 'last_name', 'email', 'password']):
            return {'message': 'No fields to update'}, 400

        # Retrieve the user from the database
        user_to_update = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user_to_update:
            return {'message': 'User not found'}, 404

        # Update the user fields
        for field, value in data.items():
            if field in ['first_name', 'last_name', 'email']:
                setattr(user_to_update, field, value)  # Dynamic attribute assignment
            elif field == 'password':
                user_to_update.password = bcrypt.generate_password_hash(value).decode('utf-8')

        # Save the updated user to the database
        db_storage.add(user_to_update)
        db_storage.commit()

        return {'message': 'User updated successfully'}, 200

class DeleteUser(Resource):
    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user
    def delete(self):
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user data from request
        email = data.get('email')
        if not email:
            return {'message': 'Missing email'}, 400

        # Check if user exists
        user_to_delete = db_storage.get_object_by_attribute(User, email=email)
        if not user_to_delete:
            return {'message': 'User not found'}, 404

        # Check if the current user is authorized to delete this user (e.g., ensure they are the same user)
        if user_to_delete.user_id != current_user_id:
            return {'message': 'Unauthorized action'}, 403

        # Delete the user
        deleted = db_storage.delete_object_by_attribute(User, email=email)
        if deleted:
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User deletion failed'}, 500

class AdminUserLogin(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user data from request
        email = data.get('email')
        password = data.get('password')

        # Check if user exists
        user = db_storage.get_object_by_attribute(User, email=email)
        if not user:
            return {'message': 'Invalid email or password'}, 401

        # Verify password hash
        if not user.password == password:
            return {'message': 'Invalid email or password'}, 401

        # Login successful, generate access token
        access_token = create_access_token(identity=user.user_id)  # Use user ID for identity

        return {'message': 'Login successful', 'access_token': access_token}, 200
