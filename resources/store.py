from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from schema import StoreSchema
from models import StoreModel
from db import db

blp = Blueprint('stores', __name__, description="Operations on stores")

@blp.route("/store")
class StoreList(MethodView):

  @blp.response(200, StoreSchema(many=True))
  def get(self):
    try:
      stores = StoreModel.query.paginate(page=1, per_page=10)
      return stores
    except SQLAlchemyError as e:
      abort(500, message=str(e))
  

  @jwt_required()
  @blp.arguments(StoreSchema)
  @blp.response(201, StoreSchema)
  def post(self, body):
    store = StoreModel(**body)
    try:
      db.session.add(store)
      db.session.commit()
      return store
    except SQLAlchemyError as e:
      abort(500, message=str(e))


@blp.route("/store/<string:storeId>")
class Store(MethodView):

  @blp.response(200, StoreSchema)
  def get(self, storeId):
    store = StoreModel.query.get_or_404(storeId)
    return store


  @jwt_required()
  @blp.arguments(StoreSchema)
  @blp.response(200, StoreSchema)
  def put(self, body, storeId):
    store = StoreModel.query.get_or_404(storeId)
    store.name = body["name"] or store.name
    try:
      db.session.add(store)
      db.session.commit()
      return store
    except SQLAlchemyError as e:
      abort(500, message=str(e))


  @jwt_required(fresh=True)
  def delete(self, storeId):
    store = StoreModel.query.get_or_404(storeId)
    try:
      db.session.delete(store)
      db.session.commit()
      return {"message": "Deleted successfully"}
    except SQLAlchemyError as e:
      abort(500, message=str(e))
