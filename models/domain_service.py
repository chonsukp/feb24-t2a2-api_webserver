from init import db, ma
from marshmallow import fields

class Domain_Service(db.Model):
    __tablename__ = "domain_services"

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)

    domain_id = db.Column(db.Integer, db.ForeignKey("domains.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)

    def __init__(self, domain_id, service_id, domain_price, service_price):
        self.domain_id = domain_id
        self.service_id = service_id
        self.total_price = domain_price + service_price

class Domain_ServiceSchema(ma.Schema):
    class Meta:
        fields = ("id", "domain_id", "service_id", "total_price", "domain", "service")

domain_service_schema = Domain_ServiceSchema()
domain_services_schema = Domain_ServiceSchema(many=True)

