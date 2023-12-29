from sqlalchemy.orm import Mapped, mapped_column
from flaskr import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    Class that represents a user of the web application

    Attributes:
        id (int) : The primary key of the user table in the database
        email (str) : The email of the user
        password (str) : The password of the user
        is_verified (bool) : Flag whether the user verified the email address
    """
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True)
    password: Mapped[str] = mapped_column(db.String)
    is_verified: Mapped[bool] = mapped_column(db.Boolean, default=False)
