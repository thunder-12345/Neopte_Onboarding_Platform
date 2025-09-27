from functools import wraps
from flask import jsonify, flash, redirect, url_for
from flask_login import current_user  

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role == permission:
                flash("You don’t have permission to access that page.")
                return redirect(url_for("user_dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator