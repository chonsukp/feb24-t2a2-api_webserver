
from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.domain import Domain, domain_schema, domains_schema

domains_bp = Blueprint("domains", __name__, url_prefix="/domains")

# /cards - GET - fetch all domains
@domains_bp.route("/")
def get_all_domains():
    stmt = db.select(Domain)
    domains = db.session.scalars(stmt)  
    return domains_schema.dump(domains)

# /cards/<id> - GET - fetch a single domain 
@domains_bp.route("/<int:domain_id>")
def get_one_domain(domain_id):
    stmt = db.select(Domain).filter_by(id=domain_id)
    domain = db.session.scalar(stmt)
    if domain:
        return domain_schema.dump(domain)
    else:
        return {"error": f"Domain with id {domain_id} not found"}, 404
    
# /cards - POST - register a new domain
@domains_bp.route("/", methods=["POST"])
@jwt_required()
def register_domain():
    body_data = request.get_json()
    domain = Domain(
        domain_name=body_data.get("domain_name"),
        registered_period=body_data.get("registered_period"),
        user_id=get_jwt_identity()
    )
    db.session.add(domain)
    db.session.commit()
    return domain_schema.dump(domain)

# /cards/<id> - DELETE - unregister a domain
@domains_bp.route("/<int:domain_id>", methods=["DELETE"])
@jwt_required()
def unregister_domain(domain_id):
    stmt = db.select(Domain).filter_by(id=domain_id)
    domain = db.session.scalar(stmt)
    if domain:
        db.session.delete(domain)
        db.session.commit()
        return {"error": f"Domain id '{domain_id}' unregistered successfully"}
    else:
        return {"error": f"Domain with id '{domain_id}' not found"}, 404

# /cards/<id> - PUT, PATCH - edit domain_name, registered_period
@domains_bp.route("/<int:domain_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_domain(domain_id):
    body_data = request.get_json()
    stmt = db.select(Domain).filter_by(id=domain_id)
    domain = db.session.scalar(stmt)
    if domain:
        domain.domain_name = body_data.get("domain_name") or domain.domain_name
        domain.registered_period = body_data.get("registered_period") or domain.registered_period
        domain.expiry_date = domain.registered_date + timedelta(days=domain.registered_period * 365) 

        db.session.commit()
        return domain_schema.dump(domain)
    else:
        return {"error": f"Domain with id '{domain_id} not found"}, 404


