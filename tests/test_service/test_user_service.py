from flaskr.service import user_service
from flaskr.models.user_model import User


def test_get_by_email_valid(test_client, init_db):
    user = user_service.get_user_by_email("userVerified@gmail.com")

    assert user is not None


def test_get_by_email_invalid(test_client, init_db):
    user = user_service.get_user_by_email("emailDoesntExist@gmail.com")
    assert user is None

    user = user_service.get_user_by_email(None)
    assert user is None


def test_add_user_valid(test_client, init_db):
    user = User(email="test@gmail.com", password="1234")
    user_service.save_user(user)
    retrieved_user = user_service.get_user_by_email("test@gmail.com")

    assert retrieved_user is not None
