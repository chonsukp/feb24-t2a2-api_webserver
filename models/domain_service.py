from init import db, ma
from marshmallow import fields


# Define the Domain_Service model for the domain_services table in the database
class Domain_Service(db.Model):
    __tablename__ = "domain_services"

    # Table columns
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)

    domain_id = db.Column(db.Integer, db.ForeignKey("domains.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)

    # Unique constraint to ensure no duplicate domain-service pairs
    __table_args__ = (db.UniqueConstraint('domain_id', 'service_id', name='_domain_service_uc'),)

     # Relationships
    domain = db.relationship("Domain", back_populates="domain_services")
    service = db.relationship("Service", back_populates="domain_services")

    # Constructor to initialise a Domain_Service instance
    def __init__(self, domain_id, service_id, domain_price, service_price):
        self.domain_id = domain_id
        self.service_id = service_id
        self.total_price = domain_price + service_price

# Define the schema for serialising and deserialising Domain_Service objects
class Domain_ServiceSchema(ma.Schema):
    # Nested relationships
    domain = fields.Nested('DomainSchema', only=["domain_name"])
    service = fields.Nested('ServiceSchema', only=["service_name"])

    class Meta:
        # Fields to include in the serialised output
        fields = ("id", "domain_id", "service_id", "total_price", "domain", "service")
        ordered = True


# Create schema instances for single and multiple domain services
domain_service_schema = Domain_ServiceSchema()
domain_services_schema = Domain_ServiceSchema(many=True)
