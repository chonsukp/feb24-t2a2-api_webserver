from flask import Blueprint

from init import db, bcrypt
from models.user import User

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
        ),
        User(
            name="User 4",
            email="user4@email.com",
            password=bcrypt.generate_password_hash("user4@123").decode("utf-8"),
        ),
        User(
            name="User 5",
            email="user5@email.com",
            password=bcrypt.generate_password_hash("user5@123").decode("utf-8"),
        ),
        User(
            name="User 6",
            email="user6@email.com",
            password=bcrypt.generate_password_hash("user6@123").decode("utf-8"),
        ),
        User(
            name="User 7",
            email="user7@email.com",
            password=bcrypt.generate_password_hash("user7@123").decode("utf-8"),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    print("Tables seeded")
