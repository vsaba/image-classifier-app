from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def logout_required(func):
    """
    A decorator function that ensures the user is not logged in

    :param func:
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in. To access this page you must logout first")
            return redirect(url_for("home.app"))
        return func(*args, **kwargs)

    return decorated_function


def verification_required(func):
    """
    A decorator function that ensures the user verified the email address

    :param func:
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_verified:
            flash("Please verify your email address!")
            return redirect(url_for('home.inactive'))
        return func(*args, *kwargs)

    return decorated_function
