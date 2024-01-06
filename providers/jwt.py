from flask_jwt_extended import JWTManager
from flask import jsonify

from models import BlockListModel

def provideJwtConfig(app):
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_cb(jwtHeader, jwtPayload):
      return (
        jsonify(
           {"message":"The token has expired", "error": "token_expired"}
        ), 
        401,
      )
    
    @jwt.invalid_token_loader
    def invalid_token_cb(error):
      return (
        jsonify(
           {"message":"The token is invalid", "error": "invalid_token"}
        ), 
        401,
      )
    
    @jwt.unauthorized_loader
    def missing_token_cb(error):
      return (
        jsonify(
          {"message":"Request doesn't contain access token", "error": "authorization_required"}
        ), 
        401,
      )


    @jwt.token_in_blocklist_loader
    def check_if_token_is_blocked(jwtHeader, jwtPayload):
      token = BlockListModel.query.filter(BlockListModel.token == jwtPayload['jti']).first()
      return bool(token)
    

    @jwt.revoked_token_loader
    def check_if_token_is_expired(jwtHeader, jwtPayload):
      return (
        jsonify(
           {"message":"The token is expired", "error": "expired_token"}
        ), 
        401,
      )
    

    return jwt
