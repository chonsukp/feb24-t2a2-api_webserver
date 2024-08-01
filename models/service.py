from init import db, ma
from marshmallow import fields


# Define the Service model for the services table in the database
class Service(db.Model):
    __tablename__ = "services"

    # Table columns
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    service_price = db.Column(db.Float, nullable=False)

    # Relationship to the Domain_Service model
    domain_services = db.relationship('Domain_Service', back_populates='service', cascade="all, delete")

# Define the schema for serialising and deserialising Service objects
class ServiceSchema(ma.Schema):
    # Nested relationship to Domain_ServiceSchema
    domain_services = fields.Nested('Domain_ServiceSchema', many=True, only=["id", "total_price"])

    class Meta:
         # Fields to include in the serialised output
        fields = ("id", "service_name", "description", "service_price", "domain_services", "domain")
        ordered = True


# Create schema instances for single and multiple services
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
