# encoding: utf-8

from flask_httpauth import HTTPBasicAuth
from flask import g
from functools import wraps
from api_service.models import User
from api_service.extensions import pwd_context

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    # TODO: Use the data in the database to validate the user credentials.
    user = User.query.filter_by(username=username).first()
    if not user or not match_passwords(password, user.password):
        return False
    g.current_user = user
    return True

def match_passwords(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.current_user.role != 'ADMIN':
            return {'message': 'You are not authorized to perform this action.'}, 403
        return func(*args, **kwargs)
    return wrapper