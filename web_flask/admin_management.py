from functools import wraps
from models.engine.db_engine import DBStorage
from models.user_model import User
from flask_jwt_extended import get_jwt_identity

db_storage = DBStorage()

def admin_user(func):
  """
  Custom decorator to check if a user is authenticated.

  Args:
      func: The function to be decorated.

  Returns:
      A wrapper function that checks for authentication before calling the original function.
  """
  @wraps(func)
  def wrapper(request, *args, **kwargs):
    current_user_id = get_jwt_identity()  # Get the current logged-in user ID

    # Retrieve the user from the database using the user_id
    user = db_storage.get_object_by_attribute(User, user_id=current_user_id)

    # Your logic to check user authentication (replace with your implementation)
    if user.confirmed:
      return func(request, *args, **kwargs)
    else:
      # Handle unauthenticated users (e.g., redirect to login page)
      return "Only Admins can perform this functions"
  return wrapper
