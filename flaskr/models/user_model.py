from sqlalchemy.orm import Mapped, mapped_column
from flaskr import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True)
    password: Mapped[str] = mapped_column(db.String)
    is_verified: Mapped[bool] = mapped_column(db.Boolean, default=False)
