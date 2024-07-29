from datetime import datetime, timedelta
from marshmallow import fields

from init import db, ma 

class Domain(db.Model):
    __tablename__ = "domains"

    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String, nullable=False, unique=True)
    registered_period = db.Column(db.Integer, nullable=False)
    registered_date = db.Column(db.Date, default=datetime.now)
    expiry_date = db.Column(db.Date, nullable=False)
    domain_price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='domains')
    domain_services = db.relationship('Domain_Service', back_populates='domain')

    def __init__(self, domain_name, registered_period, user_id):
        if not (1 <= registered_period <= 9):
            raise ValueError("Registration period must be between 1 and 9 years")
        self.domain_name = domain_name
        self.registered_period = registered_period
        self.registered_date = datetime.now().date()
        self.expiry_date = self.registered_date + timedelta(days=registered_period * 365)
        self.domain_price = self.calculate_price(registered_period)
        self.user_id = user_id

    @staticmethod
    def calculate_price(registered_period):
        prices = {
            1: 29.95,
            2: 52.95,
            3: 86.95,
            4: 113.95,
            5: 139.95,
            6: 164.95,
            7: 188.95,
            8: 211.95,
            9: 233.95
        }
        return prices.get(registered_period, 0)

class DomainSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    domain_services = fields.Nested('Domain_ServiceSchema', many=True, only=["id", "total_price"])

    class Meta:
        fields = ("id", "domain_name", "registered_period", "registered_date", "expiry_date", "domain_price", "user", "domain_services")
        ordered = True

domain_schema = DomainSchema()
domains_schema = DomainSchema(many=True)
