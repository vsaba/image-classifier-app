from flaskr.models.user_model import User


def test_create_model_default():
    user = User(email="email@", password="1234")
    assert user.email
    assert user.password
    assert user.is_verified is None


def test_create_model_verified():
    user = User(email="email@", password="1234", is_verified=True)
    assert user.email
    assert user.password
    assert user.is_verified is True
