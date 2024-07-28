from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.domain import Domain
from models.service import Service

db_commands = Blueprint("db", __name__)

# create tables
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

# drop tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

# seed tables
@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            name="Admin 1",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("admin@123").decode("utf-8"),
            is_admin=True
        ),
        User(
            name="User 1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("user1@123").decode("utf-8"),
        ),
        User(
            name="User 2",
            email="user2@email.com",
            password=bcrypt.generate_password_hash("user2@123").decode("utf-8"),
        ),
        User(
            name="User 3",
            email="user3@email.com",
            password=bcrypt.generate_password_hash("user3@123").decode("utf-8"),
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    domains = [
        Domain(
            domain_name="domain1.com.au",
            registered_period=1,
            user_id=users[1].id
        ),
        Domain(
            domain_name="domain2.com.au",
            registered_period=2,
            user_id=users[2].id
        ),
        Domain(
            domain_name="domain3.com.au",
            registered_period=3,
            user_id=users[3].id
        )
    ]

    db.session.add_all(domains)
    db.session.commit()

    services = [
        Service(
            service_name="Domain Manager", 
            description="Manage DNS records", 
            service_price=22.95
        ),
        Service(
            service_name="SSL Certification", 
            description="Encrypt website data", 
            service_price=75.95
        ),
        Service(
            service_name="Domain Privacy", 
            description="Hide WHOIS info", 
            service_price=15.95
        ),
        Service(
            service_name="Domain Redirection", 
            description="Redirect to another URL", 
            service_price=19.95
        ),
        Service(
            service_name="Email Forwarding", 
            description="Forward emails to another account", 
            service_price=30.95
        )
    ]

    db.session.add_all(services)
    db.session.commit()

    print("Tables seeded")
