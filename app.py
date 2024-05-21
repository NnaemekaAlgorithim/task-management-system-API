from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
import secrets
from web_flask.user_management import RegisterUser, LoginUser, AdminUserLogin
from web_flask.user_management import UserProfile, UpdateUser, DeleteUser
from web_flask.task_group_management import CreateTaskGroup, UpdateTaskGroup
from web_flask.task_group_management import DeleteTaskGroup, GetAllTaskGroups
from web_flask.task_management import CreateTask, GetTask, UpdateTask, DeleteTask
from flask import Flask, redirect, url_for
from flask_redoc import Redoc

# Create a Flask app
app = Flask(__name__)
CORS(app)

# Set the secret key for Flask sessions
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Set the secret key for JWT tokens
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
jwt = JWTManager(app)

@app.route('/')
def redirect_to_docs():
    return redirect(url_for('static', filename='redoc-static.html'))  # Assuming your HTML file is named redoc.html

# Create an API instance
api = Api(app)

# Register the registration and login resources with the API
api.add_resource(RegisterUser, '/register')
api.add_resource(LoginUser, '/login')
api.add_resource(AdminUserLogin, '/admin_login')
api.add_resource(UserProfile, "/user_profile")
api.add_resource(UpdateUser, '/update_user')
api.add_resource(DeleteUser, '/delete_user')
api.add_resource(CreateTaskGroup, '/create_task_group')
api.add_resource(UpdateTaskGroup, '/update_task_group')
api.add_resource(GetAllTaskGroups, '/get_all_task_groups')
api.add_resource(DeleteTaskGroup, '/delete_task_group')
api.add_resource(CreateTask, '/create_task')
api.add_resource(GetTask, '/get_tasks')
api.add_resource(UpdateTask, '/update_tasks')
api.add_resource(DeleteTask, '/delete_tasks')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
