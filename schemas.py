from marshmallow import Schema, fields


class PlainItemschema(Schema):
    id= fields.Int(dump_only=True)
    name= fields.Str(required= True)
    price=fields.Float(required= True)

class Itemupdateschema(Schema):
    name= fields.Str()
    price= fields.Float()
    store_id= fields.Int()

class Plaintagschema(Schema):
    id= fields.Int(dump_only=True)
    name= fields.Str()

class Plainstoreschema(Schema):
    id= fields.Int(dump_only=True)
    name= fields.Str(required= True)

class Itemschema(PlainItemschema):
    store_id= fields.Int(required= True,load_only=True)
    store= fields.Nested(Plainstoreschema(), dump_only= True)
    tags= fields.List(fields.Nested(Plaintagschema()), dump_only=True)

class storeschema(Plainstoreschema):
    items= fields.List(fields.Nested(PlainItemschema), dump_only= True)
    tags= fields.List(fields.Nested(Plaintagschema), dump_only= True)

class tagschema(Plaintagschema):
    store_id= fields.Int(load_only=True)
    store= fields.Nested(PlainItemschema(),dump_only= True)
    items = fields.List(fields.Nested(PlainItemschema()), dump_only= True)

class TagandItemschema(Schema):
    message= fields.Str()
    item= fields.Nested(Itemschema)
    tag= fields.Nested(tagschema)


class UserSchema(Schema):
    id= fields.Int(dump_only= True)
    username= fields.Str(required=True)
    password= fields.Str(required= True)
