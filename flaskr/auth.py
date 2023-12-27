from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .user_model import User
from .forms import RegistrationForm, LoginForm, ResetPasswordForm
from .util.decorators import logout_required

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
        # todo email verification

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Successfully registered!")
        return redirect(url_for("home.home"))
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
        return redirect(url_for("home.home"))
    return render_template("login.html", form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!")
    return redirect(url_for("home.home"))


@auth.route('/reset', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = int(current_user.get_id())
        user = db.session.scalars(db.select(User).filter_by(id=user_id)).first()

        user.password = generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Password successfully changed!")

        return redirect(url_for("home.home"))
    return render_template("reset_password.html", form=form)
