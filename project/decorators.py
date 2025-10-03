from functools import wraps
from flask import jsonify, flash, redirect, url_for
from flask_login import current_user  

ROLE_HIERARCHY = {"user": 0, "intern": 1, "volunteer": 1, "board": 2, "admin": 3}

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if ROLE_HIERARCHY.get(current_user.role, 0) < ROLE_HIERARCHY.get(permission, 5):
                flash("You don’t have permission to access that page.")

                redirect_target = {
                    "intern": "intern_dashboard",
                    "volunteer": "volunteer_dashboard",
                    "board": "board_dashboard",
                    "admin": "admin_dashboard"
                }.get(current_user.role, "user_dashboard")

                return redirect(url_for(redirect_target))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator