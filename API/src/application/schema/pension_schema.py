from marshmallow import fields
from src.application.schema.camel_case_schema import CamelCaseSchema


class PensionSchema(CamelCaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.Email(required=True) 
    max_capacity = fields.Integer(required=True)
    current_occupancy = fields.Integer(required=True)
    rating = fields.Float(required=True)
    description = fields.String(required=True)    
    image_url = fields.String(required=True)