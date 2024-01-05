from db import db
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ItemModel(db.Model):
  __tablename__ = 'items'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(80), nullable=False)
  price: Mapped[float] = mapped_column(Float(2), unique=False, nullable=False)
  store_id: Mapped[int] = mapped_column(Integer, ForeignKey('stores.id'), unique=False, nullable=False)
  store = relationship('StoreModel', back_populates='items')
  tags = relationship('TagModel', back_populates='items', secondary='items_tags')