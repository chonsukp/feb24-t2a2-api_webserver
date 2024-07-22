from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import bcrypt, db 
from models.user import User, user_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # payload of the request 
        body_data = request.get_json()
        # create an instance of the User model 
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )
        # extract password from the body
        password = body_data.get("password")

        # hash password
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # add and commit to the database
        db.session.add(user)
        db.session.commit()

        # respond back
        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address is already in use"}, 409



