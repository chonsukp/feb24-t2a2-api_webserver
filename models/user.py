from datetime import datetime
from marshmallow import fields
from marshmallow.validate import Regexp

from init import db, ma

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.Date, default=datetime.now, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    domains = db.relationship('Domain', back_populates='user')

class UserSchema(ma.Schema):
    domains = fields.List(fields.Nested('DomainSchema', exclude=["user"]))

    email = fields.String(required=True, validate=Regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', error="Invalid email format"))
    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", error="Password must be minimum eight characters, at least one letter, one number and one special character"))

    class Meta: 
        fields = ("id", "name", "email", "password", "created_date", "is_admin", "domains")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
