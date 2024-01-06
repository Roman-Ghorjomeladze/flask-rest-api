from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db import db

class UserModel(db.Model):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  password: Mapped[str] = mapped_column(String, nullable=False)