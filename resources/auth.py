from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity

from schema import AuthSchema
from models import UserModel, BlockListModel
from db import db

blp = Blueprint('auth', __name__, description="Operations on auth")

@blp.route('/auth/login')
class Login(MethodView):

  @blp.arguments(AuthSchema)
  def post(self, body):
    user = UserModel.query.filter(
      UserModel.username == body['username']
    ).first_or_404()
    if pbkdf2_sha256.verify(body['password'], user.password):
      return {
        "access_token": create_access_token(user.id, fresh=True),
        "refresh_token": create_refresh_token(user.id)
      }
    abort(400, message="Incorrect username or password")


@blp.route('/auth/register')
class Login(MethodView):

  @blp.arguments(AuthSchema)
  def post(self, body):
    duplicate = UserModel.query.filter(UserModel.username == body['username']).first()
    if duplicate:
      abort(409, message="User with such username already exists")

    password = pbkdf2_sha256.hash(body['password'])
    user = UserModel(username=body['username'], password=password)
    try:
      db.session.add(user)
      db.session.commit()
      return {"message": "Registered successfully"}
    except SQLAlchemyError as e:
      abort(500, message=str(e))


@blp.route('/auth/logout')
class Login(MethodView):
  
  @jwt_required()
  def post(self):
    token = get_jwt().get('jti')
    blockToken = BlockListModel(token=token)
    try:
      db.session.add(blockToken)
      db.session.commit()
      return {"message": "Logged out successfully"}
    except SQLAlchemyError as e:
      abort(500, str(e))
    

@blp.route('/auth/refresh')
class Refresh(MethodView):
  
  @jwt_required(refresh=True)
  def post(self):
    return {
      "access_token": create_access_token(get_jwt_identity(), fresh=False),
    }
    