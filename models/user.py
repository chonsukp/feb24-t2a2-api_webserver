from datetime import datetime
from marshmallow import fields

from init import db, ma

class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.Date, default=datetime.now, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    domains = db.relationship('Domain', back_populates='user')

class UserSchema(ma.Schema):
    domains = fields.List(fields.Nested('DomainSchema', exclude=["user"]))
    class Meta: 
        fields = ("id", "name", "email", "password", "created_date", "is_admin", "domains")

# to handle a single user object
user_schema = UserSchema(exclude=["password"])

#  to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])