from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError


# Create a Blueprint for handling errors
errors_bp = Blueprint('errors', __name__)

# Handle IntegrityError exceptions
@errors_bp.app_errorhandler(IntegrityError)
def integrity_error(error):
    # Handle unique constraint violations
    if error.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return ({"error": "This value already exists. Please use a unique value."}), 409
    
    # Handle not-null constraint violations
    if error.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        return ({"error": f"The field {error.orig.diag.column_name} is required and cannot be null."}), 409
    
    # Handle other database integrity errors
    return ({"error": "A database integrity error occurred. Please try again."}), 500

# Handle ValidationError exceptions from Marshmallow
@errors_bp.app_errorhandler(ValidationError)
def validation_error(err):
    return {"error": err.messages}, 400

# Handle ValueError exceptions
@errors_bp.app_errorhandler(ValueError)
def value_error(err):
    return {"error": str(err)}, 400

# Handle TypeError exceptions
@errors_bp.app_errorhandler(TypeError)
def type_error(err):
    return {"error": str(err)}, 400