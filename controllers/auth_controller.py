from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils import authorise_as_admin

from init import bcrypt, db 
from models.user import User, user_schema, UserSchema
from utils import auth_as_admin_decorator


# Create a Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# CREATE user
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # Load and validate the request body data
        body_data = UserSchema().load(request.get_json())
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )
        # Hash the password if provided
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Add the new user to the session and commit the transaction
        db.session.add(user)
        db.session.commit()
        # Serialise and return the new user
        return user_schema.dump(user), 201
    except IntegrityError as err:
        # Handle database integrity errors
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address is already in use"}, 409

# Log in user
@auth_bp.route("/login", methods=["POST"])
def login_user():
    # Get the request body data
    body_data = request.get_json()
     # Select the user with the given email
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # Check the password and generate a JWT token
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    else:
        return {"error": "Invalid email or password"}, 401
    
# UPDATE user (Owner and Admin only)
@auth_bp.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
# Require a valid JWT to access this route
@jwt_required()
def update_user(user_id):
    # Load and validate the request body data
    body_data = UserSchema().load(request.get_json(), partial=True)
     # Select the user with the given ID
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # Check if the user is an admin
        is_admin = authorise_as_admin()
        # Check if the user is authorised to perform the action
        if not is_admin and str(user.id) != get_jwt_identity():
            return {"error": "User is not authorised to perform this action"}, 403
        # Update the user fields
        user.name = body_data.get("name") or user.name
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # Commit
        db.session.commit()
        # Serialise and return the updated user
        return user_schema.dump(user)
    else:
        return {"error": f"User with id '{user_id}' does not exist"}, 404

# DELETE user (Admin only)
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
# Require a valid JWT to access this route
@jwt_required()
# Require admin privileges to access this route
@auth_as_admin_decorator
def delete_user(user_id):
    # Select the user with the given ID
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # Delete the user from the session and commit
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with id '{user_id}' deleted successfully"}
    else:
        return {"error": f"User with id {user_id} not found"}, 404





