from flask import Flask
from classifier.model import Classifier
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
model = Classifier()
model.load_model("classifier/mnist_model.pt")


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'My secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

    from .user_model import User

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
