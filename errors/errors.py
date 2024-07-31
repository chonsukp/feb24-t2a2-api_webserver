from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(IntegrityError)
def handle_integrity_error(error):
    if error.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return ({"error": "This value already exists. Please use a unique value."}), 409
    if error.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        return ({"error": f"The field {error.orig.diag.column_name} is required and cannot be null."}), 409
    return ({"error": "A database integrity error occurred. Please try again."}), 500

@errors_bp.app_errorhandler(ValidationError)
def validation_error(err):
    return {"error": err.messages}, 400

@errors_bp.app_errorhandler(ValueError)
def value_error(err):
    return {"error": str(err)}, 400

@errors_bp.app_errorhandler(TypeError)
def type_error(err):
    return {"error": str(err)}, 400