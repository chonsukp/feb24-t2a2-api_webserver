import functools

from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User


# Check if the current user is an admin
def authorise_as_admin():
    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()
    # Select the user from the database
    stmt = db.select(User).filter_by(id=user_id)
    # Fetch the user from the database
    user = db.session.scalar(stmt)
    # Return whether the user is an admin
    return user.is_admin

# Decorator to restrict access to admin users only
def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the current user's ID from the JWT
        user_id = get_jwt_identity()
        # Select the user from the database
        stmt = db.select(User).filter_by(id=user_id)
        # Fetch the user from the database
        user = db.session.scalar(stmt)
        # Check if the user is an admin
        if user and user.is_admin:
            # Call the decorated function if the user is an admin
            return fn(*args, **kwargs)
        else:
            # Return an error if the user is not an admin
            return {"error": "Must be admin to perform this action"}, 403
    return wrapper




