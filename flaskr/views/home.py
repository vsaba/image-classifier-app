import os

from flask import Blueprint, render_template, request, url_for, jsonify, current_app, flash, redirect
from flask_login import login_required, current_user
from flaskr.util.decorators import logout_required, verification_required
import numpy as np
from flaskr import model

hm = Blueprint('home', __name__, url_prefix='/home')


@hm.route('/', methods=['GET'])
@logout_required
def home():
    """
    The home endpoint.

    The base endpoint users that are not logged in. Renders the main page for those users.
    Requires user to be logged out.

    :return: The rendered template of the home page
    """
    return render_template("/home/home.html")


@hm.route('/app', methods=['GET'])
@login_required
@verification_required
def app():
    """
    The app endpoint.

    The base endpoint for users that are logged in. Renders the main page for those users.

    :return: The rendered template of the main app page
    """
    return render_template("/home/app.html")


@hm.route('/random', methods=['GET'])
def random_image():
    """
    Random image endpoint.

    Chooses a random image from the static directory and returns the image url in a json object

    :return: The random image url in a json object
    """
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return redirect(url_for('home.app'))

    image_directory = os.listdir(current_app.config['PATH_TO_IMAGES'])
    image = image_directory[np.random.randint(0, len(image_directory))]
    image_url = url_for('static', filename='images/' + image)

    return jsonify({"image_url": image_url})


@hm.route('/predict', methods=['POST'])
def predict_image():
    """
    The predict image endpoint.

    Loads the image from the provided image URL and runs it through the image classifier model.

    :return: The output of the image classifier model in a json format
    """
    try:
        data = request.get_json()
        image_url = os.path.basename(data.get('imagePath'))

        predicted_number = model.predict(os.path.join(current_app.config['PATH_TO_IMAGES'], image_url))

        return jsonify({'prediction': predicted_number})
    except Exception:
        flash("An error has occurred while predicting the image")
        return url_for('home.app')


@hm.route('/inactive', methods=['GET'])
@login_required
def inactive():
    """
    The inactive endpoint.

    Renders the template that a user that registered, but has not yet verified the account can view.
    Checks whether the user has verified the account in the meantime.

    :return: The render inactive template
    """
    if current_user.is_verified:
        flash("You have already verified your email address!")
        return redirect(url_for('home.app'))
    return render_template('/home/inactive.html')
