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
    image_urls = fields.List(fields.String, required=True)
    equipment = fields.String(required=True)
    opening_hours = fields.String(required=True)
    distance_km = fields.Float(dump_only=True)

    
class PensionDetailSchema(CamelCaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.Email(required=True) 
    max_capacity = fields.Integer(required=True)
    current_occupancy = fields.Integer(required=True)
    rating = fields.Float(required=True)
    description = fields.String(required=True)    
    image_urls = fields.List(fields.String, required=True)
    equipment = fields.List(fields.String, required=True)
    hours = fields.String(required=True)
    night_price = fields.Float(required=False)
    staff = fields.List(fields.Dict(keys=fields.String, values=fields.String), required=True)
    reviews = fields.List(fields.Dict(keys=fields.String, values=fields.Raw), required=True)