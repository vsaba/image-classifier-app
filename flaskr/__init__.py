from flask import Flask
from classifier.model import Classifier
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
model = Classifier()
model.load_model("classifier/mnist_model.pt")


def create_app():
    app = Flask(__name__, template_folder="../templates")

    app.config['SECRET_KEY'] = 'My secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

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
        return db.session.execute(db.select(User).filter_by(id == user_id)).first()

    return app
