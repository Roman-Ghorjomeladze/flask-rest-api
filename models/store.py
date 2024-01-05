from db import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class StoreModel(db.Model):
  __tablename__ = 'stores'

  id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
  name: Mapped[str] = mapped_column(String(80), unique=False, nullable=False)
  items = relationship('ItemModel', back_populates='store', lazy='dynamic')
  tags = relationship('TagModel', back_populates='store', lazy='dynamic')