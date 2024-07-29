from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.user import User
from models.domain import Domain
from models.service import Service
from models.domain_service import Domain_Service, domain_service_schema

domain_services_bp = Blueprint("domain_services", __name__, url_prefix="/<int:domain_id>/domain_services")

# CREATE a domain service - Admin only
@domain_services_bp.route("/", methods=["POST"])
@jwt_required()
def create_domain_service(domain_id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user.is_admin:
        return {"error": "Admin access required"}, 403

    body_data = request.get_json()
    service_id = body_data.get("service_id")

    domain_stmt = db.select(Domain).filter_by(id=domain_id)
    service_stmt = db.select(Service).filter_by(id=service_id)

    domain = db.session.scalar(domain_stmt)
    service = db.session.scalar(service_stmt)

    if domain and service:
        try:
            domain_service = Domain_Service(
                domain_id=domain.id,
                service_id=service.id,
                domain_price=domain.domain_price,
                service_price=service.service_price
            )
            db.session.add(domain_service)
            db.session.commit()
            return domain_service_schema.dump(domain_service), 201
        except IntegrityError as err:
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {"error": "This domain service combination already exists"}, 409
            else:
                return {"error": "An unexpected error occurred"}, 500
    else:
        return {"error": "Invalid domain or service ID"}, 404

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.user import User
from models.domain import Domain
from models.service import Service
from models.domain_service import Domain_Service, domain_service_schema, domain_services_schema

# DELETE a domain service - Admin only
@domain_services_bp.route("/<int:domain_service_id>", methods=["DELETE"])
@jwt_required()
def delete_domain_service(domain_id, domain_service_id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if not user.is_admin:
        return {"error": "Admin access required"}, 403

    stmt = db.select(Domain_Service).filter_by(id=domain_service_id, domain_id=domain_id)
    domain_service = db.session.scalar(stmt)
    if domain_service:
        db.session.delete(domain_service)
        db.session.commit()
        return {"message": f"Domain service id '{domain_service_id}' deleted successfully"}
    else:
        return {"error": f"Domain service with id '{domain_service_id}' not found"}, 404

