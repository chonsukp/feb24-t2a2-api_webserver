import os

from flask import Flask

from init import db, ma, bcrypt, jwt


# Create and configure the Flask application
def create_app():
    app = Flask(__name__)

    # Disable JSON key sorting
    app.json.sort_keys = False

    # Configure the SQLAlchemy database URI from environment variable
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    # Configure the JWT secret key from environment variable
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Initialise Flask extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints for cli controllers
    from controllers.cli_controlller import db_commands
    app.register_blueprint(db_commands)

    # Register blueprints for auth controllers
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    # Register blueprints for domain controllers
    from controllers.domain_controller import domains_bp
    app.register_blueprint(domains_bp)

    # Register blueprints for service controllers
    from controllers.service_controller import services_bp
    app.register_blueprint(services_bp)

    # Register blueprints for domain_service controllers
    from controllers.domain_service_controller import domain_services_bp
    app.register_blueprint(domain_services_bp)

    # Register blueprint for handling errors
    from errors.errors import errors_bp
    app.register_blueprint(errors_bp)

    return app


