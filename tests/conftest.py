import os

import pytest

from flaskr import create_app, db
from flaskr.models.user_model import User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="module")
def test_client():
    # set the testing configuration in the environment
    current_config = os.getenv('CONFIGURATION_OBJECT', default='config.Default')
    os.environ['CONFIGURATION_OBJECT'] = 'config.Testing'

    app = create_app()

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

    # reset the current environment variable from the testing variable
    os.environ['CONFIGURATION_OBJECT'] = current_config


@pytest.fixture(scope="module")
def init_db(test_client):
    db.create_all()

    user_verified = User(email="userVerified@gmail.com", password=generate_password_hash("1234"), is_verified=True)
    user_not_verified = User(email="userNotVerified@gmail.com", password=generate_password_hash("1234"))

    db.session.add(user_verified)
    db.session.add(user_not_verified)

    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="function")
def login_default_user(test_client, init_db):
    test_client.post('/auth/login', data=dict(email="userVerified@gmail.com", password="1234"))

    yield

    test_client.get('/auth/logout')
