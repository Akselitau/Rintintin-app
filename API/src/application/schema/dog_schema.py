from marshmallow import fields
from src.application.schema.camel_case_schema import CamelCaseSchema

class DogSchema(CamelCaseSchema):
    dog_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    name = fields.String(required=True)
    breed = fields.String(required=True)
    profile_photo_url = fields.String(missing=None)
    information = fields.String(missing=None)