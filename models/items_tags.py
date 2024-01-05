from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import db

class ItemsTagsModel(db.Model):
  __tablename__ = 'items_tags'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  item_id: Mapped[int] = mapped_column(Integer, ForeignKey('items.id'), nullable=False, unique=False)
  tag_id: Mapped[int] = mapped_column(Integer, ForeignKey('tags.id'), nullable=False, unique=False)