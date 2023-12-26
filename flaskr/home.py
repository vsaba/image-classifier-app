from flask import Blueprint, render_template
from flask_login import current_user

hm = Blueprint('home', __name__, url_prefix='/home')


@hm.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return render_template("app.html")
    return render_template("home.html")
