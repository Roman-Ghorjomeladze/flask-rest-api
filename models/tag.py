from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey

from db import db

class TagModel(db.Model):
  __tablename__ = "tags"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String, nullable=False)
  store_id: Mapped[int] = mapped_column(Integer, ForeignKey('stores.id'), unique=False, nullable=False)
  store = relationship('StoreModel', back_populates='tags')
  items = relationship('ItemModel', back_populates='tags', secondary='items_tags')
