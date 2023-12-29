from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .user_model import User
from .forms import RegistrationForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from .util.decorators import logout_required
from .util import token
from .util.email import send_email

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = db.session.scalars(db.select(User).filter_by(email=email)).first()
        if user:
            flash("Provided email is already in use")
            return render_template("register.html", form=form)

        new_user = User(email=email, password=generate_password_hash(password))

        verification_token = token.generate_token(new_user.email)
        confirm_url = url_for('auth.verify_reset', verification_token=verification_token, _external=True)
        html = render_template('email_body.html', confirm_url=confirm_url)

        send_email(recipient=new_user.email, subject="Verify email address", body=html)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Successfully registered! Please verify your email!")
        return redirect(url_for("home.inactive"))
    return render_template("register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = db.session.scalars(db.select(User).filter_by(email=email)).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Credentials are incorrect. Please try again")
            return render_template("login.html", form=form)

        login_user(user)
        flash("Successfully logged in!")
        return redirect(url_for("home.app"))
    return render_template("login.html", form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!")
    return redirect(url_for("home.home"))


@auth.route('/verify/<verification_token>', methods=['GET'])
def verify_reset(verification_token):
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
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = db.session.scalars(db.select(User).filter_by(email=email)).first()

        if not user:
            flash("Email invalid. Please try again.")
            return render_template("forgot_password.html", form=form)

        verification_token = token.generate_token(email)
        confirm_url = url_for("auth.reset_password", verification_token=verification_token, _external=True)
        html = render_template("email_body.html", confirm_url=confirm_url)
        send_email(recipient=email, subject="Reset password", body=html)

        flash("Email with link for password reset sent. Please check your inbox")
        return redirect(url_for("home.home"))

    return render_template("forgot_password.html", form=form)


@auth.route('/reset/<verification_token>', methods=['GET', 'POST'])
def reset_password(verification_token):
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
    return render_template("reset_password.html", form=form, verification_token=verification_token)
