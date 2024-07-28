from init import db, ma
from marshmallow import fields

class Domain_Service(db.Model):
    __tablename__ = "domain_services"

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)

    domain_id = db.Column(db.Integer, db.ForeignKey("domains.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)

    domain = db.relationship("Domain", back_populates="domain_services")
    service = db.relationship("Service", back_populates="domain_services")

    def __init__(self, domain_id, service_id, domain_price, service_price):
        self.domain_id = domain_id
        self.service_id = service_id
        self.total_price = domain_price + service_price

class Domain_ServiceSchema(ma.Schema):

    domain = fields.Nested('DomainSchema', only=["domain_name"])
    service = fields.Nested('ServiceSchema', only=["service_name"])

    class Meta:
        fields = ("id", "domain_id", "service_id", "total_price", "domain", "service")
        ordered = True

domain_service_schema = Domain_ServiceSchema()
domain_services_schema = Domain_ServiceSchema(many=True)
