from init import db, ma
from marshmallow import fields

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    service_price = db.Column(db.Float, nullable=False)

    domain_services = db.relationship('Domain_Service', back_populates='service')

class ServiceSchema(ma.Schema):

    domain_services = fields.Nested('Domain_ServiceSchema', many=True, only=["id", "total_price"])

    class Meta:
        fields = ("id", "service_name", "description", "service_price", "domain_services")
        ordered = True

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
