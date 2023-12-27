import os

from flask import Blueprint, render_template, request, url_for, jsonify, current_app, flash
from flask_login import login_required
from .util.decorators import logout_required
import numpy as np
from . import model

hm = Blueprint('home', __name__, url_prefix='/home')


@hm.route('/', methods=['GET'])
@logout_required
def home():
    return render_template("home.html")


@hm.route('/app', methods=['GET'])
@login_required
def app():
    return render_template("app.html")


@hm.route('/random', methods=['GET'])
def random_image():
    image_directory = os.listdir(current_app.config['PATH_TO_IMAGES'])
    image = image_directory[np.random.randint(0, len(image_directory))]
    image_url = url_for('static', filename='images/' + image)

    return jsonify({"image_url": image_url})


@hm.route('/predict', methods=['POST'])
def predict_image():
    try:
        data = request.get_json()
        image_url = os.path.basename(data.get('imagePath'))

        predicted_number = model.predict(os.path.join(current_app.config['PATH_TO_IMAGES'], image_url))

        return jsonify({'prediction': predicted_number})
    except Exception:
        flash("An error has occurred while predicting the image")
        return url_for('home.app')
