from marshmallow import Schema, fields

class CarSchema(Schema):
    """Class for Marshmallow serialization / deserialization"""
    id = fields.Str()
    