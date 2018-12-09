from functools import wraps
from flask import abort
from flask_login import current_user

from constants import Permission


def permission_access(permission):
    def decorator(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return decorated_func
    return decorator


def admin_access(func):
    return permission_access(Permission.ADMIN)(func)
