from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.user import User
from models.domain import Domain, domain_schema, domains_schema
from models.service import Service, services_schema
from models.domain_service import Domain_Service, domain_service_schema, domain_services_schema
from controllers.domain_service_controller import domain_services_bp

domains_bp = Blueprint("domains", __name__, url_prefix="/domains")
domains_bp.register_blueprint(domain_services_bp)

# GET all
@domains_bp.route("/")
def get_all_domains():
    stmt = db.select(Domain)
    domains = db.session.scalars(stmt)
    return domains_schema.dump(domains)

# GET one
@domains_bp.route("/<int:domain_id>")
def get_one_domain(domain_id):
    stmt = db.select(Domain).filter_by(id=domain_id)
    domain = db.session.scalar(stmt)
    if domain:
        return domain_schema.dump(domain)
    else:
        return {"error": f"Domain with id {domain_id} not found"}, 404

# CREATE
@domains_bp.route("/", methods=["POST"])
@jwt_required()
def register_domain():
    body_data = request.get_json()
    domain = Domain(
        domain_name=body_data.get("domain_name"),
        registered_period=body_data.get("registered_period"),
        user_id=get_jwt_identity()
    )
    try:
        db.session.add(domain)
        db.session.commit()
        return domain_schema.dump(domain), 201
    except IntegrityError as err:
        db.session.rollback()
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Domain name already exists"}, 409
        return {"error": "An unexpected error occurred"}, 500

# DELETE - domain owner or admin only
@domains_bp.route("/<int:domain_id>", methods=["DELETE"])
@jwt_required()
def unregister_domain(domain_id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    stmt = db.select(Domain).filter_by(id=domain_id)
    domain = db.session.scalar(stmt)
    if domain:
        if domain.user_id != user_id and not user.is_admin:
            return {"error": "You do not have permission to unregister this domain"}, 403

        try:
            db.session.delete(domain)
            db.session.commit()
            return {"message": f"Domain id '{domain_id}' unregistered successfully"}
        except IntegrityError:
            db.session.rollback()
            return {"error": "An unexpected error occurred during deletion"}, 500
    else:
        return {"error": f"Domain with id '{domain_id}' not found"}, 404

# UPDATE - domain owner or admin only
@domains_bp.route("/<int:domain_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_domain(domain_id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    stmt = db.select(Domain).filter_by(id=domain_id)
    domain = db.session.scalar(stmt)
    if domain:
        if domain.user_id != user_id and not user.is_admin:
            return {"error": "You do not have permission to update this domain"}, 403

        body_data = request.get_json()
        domain.domain_name = body_data.get("domain_name") or domain.domain_name
        domain.registered_period = body_data.get("registered_period") or domain.registered_period
        domain.expiry_date = domain.registered_date + timedelta(days=domain.registered_period * 365)

        try:
            db.session.commit()
            return domain_schema.dump(domain)
        except IntegrityError as err:
            db.session.rollback()
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {"error": "Domain name already exists"}, 409
            return {"error": "An unexpected error occurred"}, 500
    else:
        return {"error": f"Domain with id '{domain_id}' not found"}, 404
