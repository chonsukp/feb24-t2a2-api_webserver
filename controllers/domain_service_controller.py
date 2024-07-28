from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.domain import Domain
from models.service import Service
from models.domain_service import Domain_Service, domain_service_schema, domain_services_schema

domain_services_bp = Blueprint("domain_services", __name__, url_prefix="/domain_services")

# GET all domain services
@domain_services_bp.route("/", methods=["GET"])
def get_all_domain_services():
    stmt = db.select(Domain_Service)
    domain_services = db.session.scalars(stmt)
    return domain_services_schema.dump(domain_services)

# GET a single domain service by ID
@domain_services_bp.route("/<int:domain_service_id>", methods=["GET"])
def get_one_domain_service(domain_service_id):
    stmt = db.select(Domain_Service).filter_by(id=domain_service_id)
    domain_service = db.session.scalar(stmt)
    if domain_service:
        return domain_service_schema.dump(domain_service)
    else:
        return {"error": f"Domain_Service with id {domain_service_id} not found"}, 404

# POST create a new domain service
@domain_services_bp.route("/", methods=["POST"])
@jwt_required()
def create_domain_service():
    body_data = request.get_json()
    domain_id = body_data.get("domain_id")
    service_id = body_data.get("service_id")

    domain_stmt = db.select(Domain).filter_by(id=domain_id)
    service_stmt = db.select(Service).filter_by(id=service_id)

    domain = db.session.scalar(domain_stmt)
    service = db.session.scalar(service_stmt)

    if domain and service:
        domain_service = Domain_Service(
            domain_id=domain.id,
            service_id=service.id,
            domain_price=domain.domain_price,
            service_price=service.service_price
        )
        db.session.add(domain_service)
        db.session.commit()
        return domain_service_schema.dump(domain_service), 201
    else:
        return {"error": "Invalid domain or service ID"}, 404

# DELETE a domain service by ID
@domain_services_bp.route("/<int:domain_service_id>", methods=["DELETE"])
@jwt_required()
def delete_domain_service(domain_service_id):
    stmt = db.select(Domain_Service).filter_by(id=domain_service_id)
    domain_service = db.session.scalar(stmt)
    if domain_service:
        db.session.delete(domain_service)
        db.session.commit()
        return {"message": f"Domain_Service id '{domain_service_id}' deleted successfully"}
    else:
        return {"error": f"Domain_Service with id '{domain_service_id}' not found"}, 404

