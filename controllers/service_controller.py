from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user import User
from models.service import Service, service_schema, services_schema

services_bp = Blueprint("services", __name__, url_prefix="/services")

# GET all services
@services_bp.route("/", methods=["GET"])
def get_all_services():
    stmt = db.select(Service)
    services = db.session.scalars(stmt)
    return services_schema.dump(services)

# GET a single service by ID
@services_bp.route("/<int:service_id>", methods=["GET"])
def get_one_service(service_id):
    stmt = db.select(Service).filter_by(id=service_id)
    service = db.session.scalar(stmt)
    if service:
        return service_schema.dump(service)
    else:
        return {"error": f"Service with id '{service_id}' not found"}, 404

# POST create a new service - Admin only
@services_bp.route("/", methods=["POST"])
@jwt_required()
def create_service():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user.is_admin:
        return {"error": "Admin access required"}, 403

    body_data = request.get_json()
    service = Service(
        service_name=body_data.get("service_name"),
        description=body_data.get("description"),
        service_price=body_data.get("service_price")
    )
    db.session.add(service)
    db.session.commit()
    return service_schema.dump(service), 201

# PUT/PATCH update a service by ID - Admin only
@services_bp.route("/<int:service_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_service(service_id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user.is_admin:
        return {"error": "Admin access required"}, 403

    body_data = request.get_json()
    stmt = db.select(Service).filter_by(id=service_id)
    service = db.session.scalar(stmt)
    if service:
        service.service_name = body_data.get("service_name") or service.service_name
        service.description = body_data.get("description") or service.description
        service.service_price = body_data.get("service_price") or service.service_price

        db.session.commit()
        return service_schema.dump(service)
    else:
        return {"error": f"Service with id '{service_id}' not found"}, 404
    
# DELETE a service by ID - Admin only
@services_bp.route("/<int:service_id>", methods=["DELETE"])
@jwt_required()
def delete_service(service_id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user.is_admin:
        return {"error": "Admin access required"}, 403

    stmt = db.select(Service).filter_by(id=service_id)
    service = db.session.scalar(stmt)
    if service:
        db.session.delete(service)
        db.session.commit()
        return {"message": f"Service id '{service_id}' deleted successfully"}
    else:
        return {"error": f"Service with id '{service_id}' not found"}, 404
