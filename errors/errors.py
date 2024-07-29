from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(IntegrityError)
def handle_integrity_error(error):
    if error.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return jsonify({"error": "This value already exists. Please use a unique value."}), 409
    if error.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        return jsonify({"error": f"The field {error.orig.diag.column_name} is required and cannot be null."}), 409
    return jsonify({"error": "A database integrity error occurred. Please try again."}), 500

@errors_bp.app_errorhandler(404)
def handle_not_found_error(error):
    return jsonify({"error": "The requested resource could not be found."}), 404

@errors_bp.app_errorhandler(403)
def handle_forbidden_error(error):
    return jsonify({"error": "You do not have permission to access this resource."}), 403

@errors_bp.app_errorhandler(500)
def handle_internal_server_error(error):
    return jsonify({"error": "An unexpected server error occurred. Please try again later."}), 500

@errors_bp.app_errorhandler(Exception)
def handle_generic_error(error):
    return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
