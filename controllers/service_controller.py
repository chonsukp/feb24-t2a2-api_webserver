from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user import User
from models.service import Service, service_schema, services_schema
from utils import auth_as_admin_decorator


# Create a Blueprint for the services routes
services_bp = Blueprint("services", __name__, url_prefix="/services")

# GET all services
@services_bp.route("/", methods=["GET"])
def get_all_services():
    # Select all services from the database
    stmt = db.select(Service)
    # Execute the query and get the results
    services = db.session.scalars(stmt)
    # Serialise and return the results
    return services_schema.dump(services)

# GET one service by ID
@services_bp.route("/<int:service_id>", methods=["GET"])
def get_one_service(service_id):
    # Select the service with the given ID
    stmt = db.select(Service).filter_by(id=service_id)
    # Execute the query and get the result
    service = db.session.scalar(stmt)
    if service:
        # Serialise and return the service
        return service_schema.dump(service)
    else:
        # Return error if service not found
        return {"error": f"Service with id '{service_id}' not found"}, 404

# CRETE a new service (Admin only)
@services_bp.route("/", methods=["POST"])
# Require a valid JWT to access this route
@jwt_required()
# Require admin privileges to access this route
@auth_as_admin_decorator
def create_service():
    # Get the request body data
    body_data = request.get_json()
    # Check for required fields
    if 'service_name' not in body_data:
        return {"error": "Service name field is required"}, 400
    if 'description' not in body_data:
        return {"error": "Description field is required"}, 400
    if 'service_price' not in body_data:
        return {"error": "Service price field is required"}, 400
    
    # Create a new Service instance
    service = Service(
        service_name=body_data.get("service_name"),
        description=body_data.get("description"),
        service_price=body_data.get("service_price")
    )
    # Add the service to the session and commit
    db.session.add(service)
    db.session.commit()
    # Serialise and return the new service
    return service_schema.dump(service), 201

# UPDATE service (Admin Only)
@services_bp.route("/<int:service_id>", methods=["PUT", "PATCH"])
# Require a valid JWT to access this route
@jwt_required()
# Require admin privileges to access this route
@auth_as_admin_decorator
def update_service(service_id):
    # Get the request body data
    body_data = request.get_json()
    # Select the service with the given ID
    stmt = db.select(Service).filter_by(id=service_id)
    # Execute the query and get the result
    service = db.session.scalar(stmt)
    if service:
        # Update the service fields with new data or keep the old data
        service.service_name = body_data.get("service_name") or service.service_name
        service.description = body_data.get("description") or service.description
        service.service_price = body_data.get("service_price") or service.service_price

        # Commit
        db.session.commit()
        # Serialise and return the updated service
        return service_schema.dump(service)
    else:
        # Return error if service not found
        return {"error": f"Service with id '{service_id}' not found"}, 404

# DELETE service (Admin only)
@services_bp.route("/<int:service_id>", methods=["DELETE"])
# Require a valid JWT to access this route
@jwt_required()
# Require admin privileges to access this route
@auth_as_admin_decorator
def delete_service(service_id):
    # Select the service with the given ID
    stmt = db.select(Service).filter_by(id=service_id)
    # Execute the query and get the result
    service = db.session.scalar(stmt)
    if service:
        # Delete the service from the session and commit
        db.session.delete(service)
        db.session.commit()
        # Return success message
        return {"message": f"Service id '{service_id}' deleted successfully"}
    else:
        # Return error if service not found
        return {"error": f"Service with id '{service_id}' not found"}, 404
    

