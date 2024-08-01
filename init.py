from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


# Initialise Flask extensions
# Database interactions
db = SQLAlchemy()
# Object serialisation/deserialisation
ma = Marshmallow()
# Password hashing
bcrypt = Bcrypt()
# Handling JSON Web Tokens
jwt = JWTManager()
