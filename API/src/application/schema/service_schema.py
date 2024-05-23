from marshmallow import fields
from chalicelib.application.schema.camel_case_schema import CamelCaseSchema

class ServiceSchema(CamelCaseSchema):    
    id = fields.Integer(required=True)
    pension_id = fields.Integer(required=True)
    price = fields.Integer(required=True)
    description = fields.String(required=True)
