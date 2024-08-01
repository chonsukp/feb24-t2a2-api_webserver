from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user import User
from models.domain import Domain
from models.service import Service
from models.domain_service import Domain_Service, domain_service_schema
from utils import auth_as_admin_decorator

# Create a Blueprint for the domain services routes
domain_services_bp = Blueprint("domain_services", __name__, url_prefix="/<int:domain_id>/domain_services")

# CREATE domain service (Admin Only)
@domain_services_bp.route("/", methods=["POST"])
# Require a valid JWT to access this route
@jwt_required()
# Require admin privileges to access this route
@auth_as_admin_decorator
def create_domain_service(domain_id):
    # Get the request body data
    body_data = request.get_json()
    # Get the service ID from the request body
    service_id = body_data.get("service_id")
    # Select the domain and service from the database
    domain_stmt = db.select(Domain).filter_by(id=domain_id)
    service_stmt = db.select(Service).filter_by(id=service_id)
    # Execute the query and get the domain
    domain = db.session.scalar(domain_stmt)
    # Execute the query and get the service
    service = db.session.scalar(service_stmt)
    if domain and service:
        # Create a new Domain_Service instance
        domain_service = Domain_Service(
            domain_id=domain.id,
            service_id=service.id,
            domain_price=domain.domain_price,
            service_price=service.service_price
        )
        # Add the domain service to the session and commit
        db.session.add(domain_service)
        db.session.commit()
        # Serialise and return the new domain service
        return domain_service_schema.dump(domain_service), 201
    else:
        # Return error if domain or service not found
        return {"error": "Invalid domain or service ID"}, 404

# DELETE domain service (Admin only)
@domain_services_bp.route("/<int:domain_service_id>", methods=["DELETE"])
# Require a valid JWT to access this route
@jwt_required()
# Require admin privileges to access this route
@auth_as_admin_decorator
def delete_domain_service(domain_id, domain_service_id):
    # Select the domain service with the given ID and domain ID from the database
    stmt = db.select(Domain_Service).filter_by(id=domain_service_id, domain_id=domain_id)
    # Execute the query and get the domain service
    domain_service = db.session.scalar(stmt)
    if domain_service:
        # Delete the domain service from the session and commit
        db.session.delete(domain_service)
        db.session.commit()
        # Return success message
        return {"message": f"Domain service id '{domain_service_id}' deleted successfully"}
    else:
        # Return error if domain service not found
        return {"error": f"Domain service with id '{domain_service_id}' not found"}, 404
