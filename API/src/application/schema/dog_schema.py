from marshmallow import fields, post_dump
from chalicelib.application.schema.camel_case_schema import CamelCaseSchema



class DogSchema(CamelCaseSchema):
    id = fields.Integer(required=True)
    owner_id = fields.Integer(required=True)
    name = fields.String(required=True)
    breed = fields.String(required=True)
    age = fields.Integer(required=True) 
    weight = fields.Integer(required=False)
    special_needs = fields.String(required=True)


