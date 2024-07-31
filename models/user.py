from datetime import datetime 

from marshmallow import fields 
from marshmallow.validate import Regexp

from init import db, ma 


# Define the User model for the users table in the database
class User(db.Model):
    __tablename__ = "users"

   # Table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.Date, default=datetime.now, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationship to the Domain model
    domains = db.relationship('Domain', back_populates='user', cascade="all, delete")


# Define the schema for serializing and deserializing User objects
class UserSchema(ma.Schema):
    # Nested relationship to DomainSchema
    domains = fields.List(fields.Nested('DomainSchema', exclude=["user"]))

    # Field validation for email and password
    email = fields.String(
        required=True,
          validate=Regexp(
              '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
              error="Invalid email format"
        )
    )
    password = fields.String(
        required=True, validate=Regexp(
            "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            error="Password must be minimum eight characters, at least one letter, one number and one special character"
        )
    )

    class Meta: 
        # Fields to include in the serialized output
        fields = ("id", "name", "email", "password", "created_date", "is_admin", "domains")


# Create schema instances for single and multiple users, excluding the password field
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
