from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user import User
from models.domain import Domain, domain_schema, domains_schema
from models.domain_service import Domain_Service, domain_service_schema, domain_services_schema
from controllers.domain_service_controller import domain_services_bp
from utils import authorise_as_admin


# Create a Blueprint for the domains routes
domains_bp = Blueprint("domains", __name__, url_prefix="/domains")
domains_bp.register_blueprint(domain_services_bp)

# GET all domains
@domains_bp.route("/")
def get_all_domains():
    # Select all domains from the database
    stmt = db.select(Domain) 
    # Execute the query and get the results
    domains = db.session.scalars(stmt) 
    # Serialise and return the results
    return domains_schema.dump(domains) 

# GET one domain
@domains_bp.route("/<int:domain_id>")
def get_one_domain(domain_id):
    # Select the domain with the given ID
    stmt = db.select(Domain).filter_by(id=domain_id)
    # Execute the query and get the result
    domain = db.session.scalar(stmt)
    if domain:
        # Serialise and return the domain
        return domain_schema.dump(domain)
    else:
        # Return error if domain not found
        return {"error": f"Domain with id {domain_id} not found"}, 404

# CREATE domain
@domains_bp.route("/", methods=["POST"])
# Require a valid JWT to access this route
@jwt_required()
def register_domain():
    # Load and validate the request body data
    body_data = domain_schema.load(request.get_json())
    if 'registered_period' not in body_data:
        # Return error if registered period is missing
        return {"error": "registered period is required"}, 400
    domain = Domain(
        domain_name=body_data.get("domain_name"),
        registered_period=body_data.get("registered_period"),
        user_id=get_jwt_identity()
    )
    # Add the new domain to the session and commit
    db.session.add(domain)
    db.session.commit()
    # Serialise and return the new domain
    return domain_schema.dump(domain), 201

# UPDATE domain (Owner and Admin only)
@domains_bp.route("/<int:domain_id>", methods=["PUT", "PATCH"])
# Require a valid JWT to access this route
@jwt_required()
def update_domain(domain_id):
    # Load and validate the request body data
    body_data = domain_schema.load(request.get_json(), partial=True)
    # Select the domain with the given ID
    stmt = db.select(Domain).filter_by(id=domain_id)
    # Execute the query and get the result
    domain = db.session.scalar(stmt)
    if domain:
        # Check if the user is an admin
        is_admin = authorise_as_admin()
        if not is_admin and str(domain.user_id) != get_jwt_identity():
            # Return error if not authorised
            return {"error": "User is not authorised to perform this action"}, 403
        domain.domain_name = body_data.get("domain_name") or domain.domain_name
        domain.expiry_date = domain.registered_date + timedelta(days=domain.registered_period * 365)
        # Commit
        db.session.commit()
        # Serialise and return the updated domain
        return domain_schema.dump(domain)
    else:
        # Return error if domain not found
        return {"error": f"Domain with id '{domain_id}' not found"}, 404

# DELETE domain (Owner and Admin only)
@domains_bp.route("/<int:domain_id>", methods=["DELETE"])
# Require a valid JWT to access this route
@jwt_required()
def delete_domain(domain_id):
    # Select the domain with the given ID
    stmt = db.select(Domain).filter_by(id=domain_id)
    # Execute the query and get the result
    domain = db.session.scalar(stmt)
    if domain:
        # Check if the user is an admin
        is_admin = authorise_as_admin()
        if not is_admin and str(domain.user_id) != get_jwt_identity():
            # Return error if not authorised
            return {"error": "User is not authorised to perform this action."}, 403
        # Delete the domain from the session and commit 
        db.session.delete(domain)
        db.session.commit()
        # Return success message
        return {"message": f"Domain with id '{domain_id}' deleted successfully"}
    else:
        # Return error if domain not found
        return {"error": f"Domain with id '{domain_id}' not found"}, 404