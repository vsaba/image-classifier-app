import os

from flask import Blueprint, render_template, request, url_for, jsonify, current_app, flash, redirect
from flask_login import login_required, current_user
from flaskr.util.decorators import logout_required, verification_required
import numpy as np
from flaskr import model
from flaskr.util import email

hm = Blueprint('home', __name__, url_prefix='/home')


@hm.route('/', methods=['GET'])
@logout_required
def home():
    return render_template("/home/home.html")


@hm.route('/app', methods=['GET'])
@login_required
@verification_required
def app():
    return render_template("/home/app.html")


@hm.route('/random', methods=['GET'])
def random_image():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return redirect(url_for('home.app'))

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


@hm.route('/inactive', methods=['GET'])
@login_required
def inactive():
    if current_user.is_verified:
        flash("You have already verified your email address!")
        return redirect(url_for('home.app'))
    return render_template('/home/inactive.html')
