from flaskr import db
from flaskr.models.user_model import User


def get_user_by_email(email: str):
    """
    Retrieves a user from the database by the provided email

    :param email: The provided user email
    :return: Returns a User instance if email exists, returns none otherwise
    """
    if email is None:
        return None

    user = db.session.scalars(db.select(User).filter_by(email=email)).first()

    return user


def save_user(user: User):
    """
    Saves the provided User instance to the database

    :param user: The provided User instance
    :return: If provided instance is None, returns without saving to the database
    """
    if user is None:
        return
    db.session.add(user)
    db.session.commit()
