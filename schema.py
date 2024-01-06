from marshmallow import Schema, fields, ValidationError, validates
import re
class PlainItemSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  price = fields.Float(required=True)

class PlainStoreSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)

class PlainTagSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
  name = fields.Str()
  price = fields.Float()

class ItemSchema(PlainItemSchema):
  store_id = fields.Int(required=True, load_only=True)
  store = fields.Nested(PlainStoreSchema(), dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
  items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
  store_id = fields.Int(dump_only=True)
  store = fields.Nested(PlainStoreSchema(), dump_only=True)
  items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  password = fields.Str(required=True)

def isValidPassword(value):
  print(value)
  return True
class AuthSchema(Schema):
  username = fields.Str(required=True)
  password = fields.Str(required=True, validate=isValidPassword)