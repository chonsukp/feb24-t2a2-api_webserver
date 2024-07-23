from datetime import datetime, timedelta
from marshmallow import fields

from init import db, ma 

class Domain(db.Model):
    __tablename__ = "domains"

    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String, nullable=False, unique=True)
    registered_period =  db.Column(db.Integer, nullable=False)
    registered_date = db.Column(db.Date, default=datetime.now)
    expiry_date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='domains')

    # initialise new object to calculate the registration and expiry dates fo the domain
    def __init__(self, domain_name, registered_period, user_id):
        if not (1 <= registered_period <= 9):
            raise ValueError("Registration period must be between 1 and 9 years")
        self.domain_name = domain_name
        self.registered_period = registered_period
        self.registered_date = datetime.now().date()
        self.expiry_date = self.registered_date + timedelta(days=registered_period * 365)
        self.user_id = user_id

    class DomainSchema(ma.Schema):

        user = fields.Nested('UserSchema', only=["id", "name", "email"])

        class Meta:
            fields = ("id", "domain_name", "registered_period", "registered_date", "expiry_date", "user_id")

    domain_schema = DomainSchema()
    domains_schema = DomainSchema(many=True)

  
    

    