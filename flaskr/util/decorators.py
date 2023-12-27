# todo dodati logout_required decorator sa flask-login
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in. To access this page you must logout first")
            return redirect(url_for("home.app"))
        return func(*args, **kwargs)

    return decorated_function
