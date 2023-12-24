from sqlalchemy.orm import Mapped, mapped_column
from . import db


class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True)
    password: Mapped[str] = mapped_column(db.String)
