from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import TagModel
from models import StoreModel, ItemModel
from schema import TagSchema, ItemSchema
from db import db

blp = Blueprint('tag', __name__, description = "Operations on tags")
@blp.route("/store/<string:storeId>/tag")
class ListTags(MethodView):
  def get(self, storeId):
    store = StoreModel.query.first_or_404(storeId)
    tags = store.tags.all()
    return tags
  

  @jwt_required()
  @blp.arguments(TagSchema)
  @blp.response(201, TagSchema)
  def post(self, body, storeId):
    tag = TagModel(store_id=storeId, **body)
    try:
      db.session.add(tag)
      db.session.commit()
      return tag
    except SQLAlchemyError as e:
      abort(500, str(e))


@blp.route("/item/<string:itemId>/tag/<string:tagId>")
class LinkTagsToItem(MethodView):

  @jwt_required()
  @blp.response(200, ItemSchema)
  def post(self, itemId, tagId):
    item = ItemModel.query.get_or_404(itemId)
    tag = TagModel.query.get_or_404(tagId)
    if item.store_id != tag.store_id:
      abort(400, message="You can't add tag from a different store")
    item.tags.append(tag)
    try:
      db.session.add(item)
      db.session.commit()
      return item
    except SQLAlchemyError as e:
      abort(500, message=str(e))


  @jwt_required()
  @blp.response(200, ItemSchema)
  def delete(self, itemId, tagId):
    item = ItemModel.query.get_or_404(itemId)
    tag = TagModel.query.get_or_404(tagId)
    item.tags.remove(tag)
    try:
      db.session.add(item)
      db.session.commit()
      return item
    except SQLAlchemyError as e:
      abort(500, message=str(e))


@blp.route('/tag/<string:tagId>')
class Tag(MethodView):

  @blp.response(200, TagSchema)
  def get(self, tagId):
    tag = TagModel.query.get_or_404(tagId)
    return tag
  

  @jwt_required(fresh=True)
  def delete(self, tagId):
    tag = TagModel.query.get_or_404(tagId)
    try:
      db.session.delete(tag)
      db.session.commit()
      return {"message": "Deleted successfully"}
    except SQLAlchemyError as e:
      abort(500, str(e))