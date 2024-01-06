from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from models import ItemModel
from schema import ItemSchema, ItemUpdateSchema
from db import db

blp = Blueprint('item', __name__, description="Operations on items")

@blp.route("/item")
class ItemList(MethodView):

  @blp.response(200, ItemSchema(many=True))
  def get(self):
    try:
      items = ItemModel.query.paginate(page=1, per_page=10)
      return items
    except SQLAlchemyError as e:
      abort(500, message=str(e))


  @jwt_required()
  @blp.arguments(ItemSchema)
  @blp.response(201, ItemSchema)
  def post(self, body):
    item = ItemModel(**body)
    try:
      db.session.add(item)
      db.session.commit()
      return item
    except SQLAlchemyError as e:
      abort(500, message=str(e))


@blp.route("/item/<string:itemId>")
class Item(MethodView):
  @blp.response(200, ItemSchema)
  def get(self, itemId):
    try:
      item = ItemModel.query.get_or_404(itemId)
      return item
    except SQLAlchemyError as e:
      abort(500, message=str(e))
    

  @jwt_required()
  @blp.arguments(ItemUpdateSchema)
  @blp.response(200, ItemSchema)
  def put(self, body, itemId):
    item = ItemModel.query.get_or_404(itemId)
    item.name = body["name"] or item.name
    item.price = body["price"] or item.price
    try:
      db.session.add(item)
      db.session.commit()
      return item
    except SQLAlchemyError as e:
      abort(500, message=str(e))
  

  @jwt_required(fresh=True)
  def delete(self, itemId):
    item = ItemModel.query.get_or_404(itemId)
    try:
      db.session.delete(item)
      db.session.commit()
      return {"message": "Deleted succesfully"}
    except SQLAlchemyError as e:
      abort(500, message=str(e))