# encoding: utf-8

from flask_httpauth import HTTPBasicAuth
from flask import g, abort
from functools import wraps
from api_service.models import User
from api_service.extensions import pwd_context

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not match_passwords(password, user.password):
        return False
    g.current_user = user
    return True

def match_passwords(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def admin_required(func):
    """ 
    Decorator to check if the user is an admin
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.current_user.role != 'ADMIN':
            abort(403, description='You are not authorized to perform this action.')
        return func(*args, **kwargs)
    return wrapper