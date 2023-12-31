from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models.user_model import User
from flaskr.models.forms import RegistrationForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from flaskr.util.decorators import logout_required
from flaskr.util import token
from flaskr.util.email import send_email, compose_email

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    """
    The register endpoint.

    If request method is GET, creates the RegistrationForm and renders the html template for user registration.
    If request method is POST, validates the form, checks if the email provided in the form already exists,
    creates a new user, sends verification email and commits user to the database.
    Requires user to be logged out to access the endpoint.

    :return: Register template, or reroutes to inactive page if registration successful
    """
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = db.session.scalars(db.select(User).filter_by(email=email)).first()
        if user:
            flash("Provided email is already in use")
            return render_template("/auth/register.html", form=form)

        new_user = User(email=email, password=generate_password_hash(password))

        verification_token = token.generate_token(new_user.email)
        body = compose_email(verification_token=verification_token, url='auth.verify_reset',
                             template_path='/email/account_verify_email.html')
        send_email(recipient=new_user.email, subject="Verify email address", body=body)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Successfully registered! Please verify your email!")
        return redirect(url_for("home.inactive"))
    return render_template("/auth/register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    """
    The login endpoint.

    If request method is GET, creates the LoginForm and renders the login template.
    If request method is POST, validates the form, verifies the provided credentials and logs in user.
    Requires user to be logged out to access the endpoint.

    :return: The login template, or if login successful reroutes to home page
    """
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = db.session.scalars(db.select(User).filter_by(email=email)).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Credentials are incorrect. Please try again")
            return render_template("/auth/login.html", form=form)

        login_user(user)
        flash("Successfully logged in!")
        return redirect(url_for("home.app"))
    return render_template("/auth/login.html", form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    The logout endpoint.

    Logs out the user from the session. Requires user to be logged in to access the endpoint

    :return: Redirects to home endpoint
    """
    logout_user()
    flash("Logged out successfully!")
    return redirect(url_for("home.home"))


@auth.route('/verify/<verification_token>', methods=['GET'])
def verify_reset(verification_token):
    """
    The token verification endpoint.

    Verifies the provided verification_token param. If verification is successful,
    activates the user and commits the modified user to the database.

    :param verification_token: The verification token to be decoded
    :return: Redirects to home page if email confirmation is successful, otherwise redirects to inactive page.
    """
    if current_user.is_verified:
        flash("You have already verified your email address")
        return redirect(url_for('home.app'))
    user_email = token.verify_token(verification_token)
    user = db.session.scalars(db.select(User).filter_by(email=user_email)).first()
    if user.email == user_email:
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        flash("Email successfully verified. Enjoy using the app")
        return redirect(url_for('home.app'))

    flash("An error occurred while verifying. Please check your inbox and try again")
    return redirect(url_for('home.inactive'))


@auth.route('/forgot', methods=['GET', 'POST'])
@logout_required
def forgot_password():
    """
    The forgot password endpoint.

    If request method is GET, creates the ForgotPasswordForm and renders the form in the forgot password template.
    If request method is POST, validates the provided for, verifies the provided data and sends an email with
    an url for password reset.
    Requires user to be logged out to access the endpoint.

    :return: Renders the forgot password template, or redirects to the home page if POST method is used
    """
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = db.session.scalars(db.select(User).filter_by(email=email)).first()

        if not user:
            flash("Email invalid. Please try again.")
            return render_template("/auth/forgot_password.html", form=form)

        verification_token = token.generate_token(email)
        body = compose_email(verification_token=verification_token, url='auth.reset_password',
                             template_path="/email/forgot_password_email.html")
        send_email(recipient=email, subject="Reset password", body=body)

        flash("Email with link for password reset sent. Please check your inbox")
        return redirect(url_for("home.home"))

    return render_template("/auth/forgot_password.html", form=form)


@auth.route('/reset/<verification_token>', methods=['GET', 'POST'])
def reset_password(verification_token):
    """
    The reset password endpoint.

    Verifies the provided verification token. If token decoding is not successful,
    redirects the user to the forgot password endpoint.
    If request method is GET, creates the ForgotPasswordForm and renders it in the forgot password template.
    If request method is POST, validates the form, changes the password of
    the user object and commits the new user to the database.

    :param verification_token: The verification token to be decoded
    :return: Renders the forgot password template, or if method is POST redirects to home page.
    """
    email = token.verify_token(verification_token)

    if not email:
        flash("An error occurred while validating. Please enter your email and try again")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.session.scalars(db.select(User).filter_by(email=email)).first()
        user.password = generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Password successfully changed!")

        return redirect(url_for("home.home"))
    return render_template("/auth/reset_password.html", form=form, verification_token=verification_token)
