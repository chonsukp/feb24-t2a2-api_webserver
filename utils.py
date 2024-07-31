import functools

from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User

def authorise_as_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin

def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user and user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {"error": "Must be admin to perform this action"}, 403
    return wrapper




