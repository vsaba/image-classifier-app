from flask import Flask
from classifier.model import Classifier
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
model = Classifier()
mail = Mail()


def create_app():
    """
    Factory method that creates a Flask app instance, loads configurations,
    assigns blueprints and initializes the database

    :return: The app instance
    """
    app = Flask(__name__)

    app.config.from_object('config')

    model.load_model("classifier/mnist_model.pt")
    mail.init_app(app)

    from flaskr.models.user_model import User

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .views.home import hm as home_blueprint
    app.register_blueprint(home_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalars(db.select(User).filter_by(id=int(user_id))).first()

    return app
