from flask import Flask
from flask_smorest import Api
from datetime import timedelta
import os

from resources.item import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint
from resources.tag import blp as TagsBluePrint
from resources.auth import blp as AuthBluePrint
from providers.jwt import provideJwtConfig
from db import db

def create_app(db_url=None):
  app = Flask(__name__)

  app.config["PROPAGATE_EXCEPTIONS"] = True
  app.config["API_TITLE"] = "Stores REST API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.3"
  app.config["OPENAPI_URL_PREFIX"] = "/"
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
  app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.init_app(app)
  api = Api(app)

  app.config["JWT_SECRET_KEY"] = "SOME_RANDOM_STRING_FROM_ENV"
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
  
  provideJwtConfig(app)
  with app.app_context():
    db.create_all()

  api.register_blueprint(ItemBluePrint)
  api.register_blueprint(StoreBluePrint)
  api.register_blueprint(TagsBluePrint)
  api.register_blueprint(AuthBluePrint)

  return app