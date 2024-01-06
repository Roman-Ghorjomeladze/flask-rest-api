from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from db import db

class BlockListModel(db.Model):
  __tablename__ = 'blocklist'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  token: Mapped[str] = mapped_column(String, nullable=False, unique=False, index=True)