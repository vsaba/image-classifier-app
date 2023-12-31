from flask import render_template


def bad_request_handler(e):
    error_title = "A bad request has occurred!"
    error_body = "Whoops... A bad request seems to have been made. Please try again."
    return render_template("/error/error.html", error_title=error_title, error_body=error_body), 400


def unauthorized_handler(e):
    error_title = "Unauthorized access!"
    error_body = ("""Whoops... It seems your are not authorized to view this page.
                  Please log-in or register in order to access this page""")
    return render_template("/error/error.html", error_title=error_title, error_body=error_body), 401


def forbidden_handler(e):
    error_title = "This request is forbidden"
    error_body = ("We are sorry, we understand what you sent us but you are forbidden from doing those actions. Its "
                  "not you its us.. you know how it is.")
    return render_template("/error/error.html", error_title=error_title, error_body=error_body), 403


def not_found_handler(e):
    error_title = "Wait, where is it?"
    error_body = ("Well, this is awkward, we are unable to find the page you are looking for. Are you sure you entered "
                  "the right route?")
    return render_template("/error/error.html", error_title=error_title, error_body=error_body), 404


def method_not_allowed_handler(e):
    error_title = "Yeah, this method is not allowed..."
    error_body = ("It seems you used the wrong method to send us something, please look into it and try again, "
                  "we will wait!")
    return render_template("/error/error.html", error_title=error_title, error_body=error_body), 405


def internal_server_error_handler(e):
    error_title = "Well, this is awkward."
    error_body = ("It seems there is a small mistake on our part. We are sorry for the inconvenience, we are trying to "
                  "solve it as fast as we can!")
    return render_template("/error/error.html", error_title=error_title, error_body=error_body), 500
