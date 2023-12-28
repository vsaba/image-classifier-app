from flask import Flask
from classifier.model import Classifier
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
model = Classifier()
model.load_model("classifier/mnist_model.pt")
mail = Mail()


def create_app():
    app = Flask(__name__, template_folder="../templates")

    app.config['SECRET_KEY'] = 'My secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['PATH_TO_IMAGES'] = "flaskr/static/images"

    app.config['TOKEN_SERIALIZER_SALT'] = 'token_salt'

    app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'ac8aa3a417d060'
    app.config['MAIL_PASSWORD'] = '7b492d3ee09491'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail.init_app(app)

    from .user_model import User

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .home import hm as home_blueprint
    app.register_blueprint(home_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalars(db.select(User).filter_by(id=int(user_id))).first()

    return app
