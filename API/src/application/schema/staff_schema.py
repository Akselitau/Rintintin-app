from marshmallow import fields
from chalicelib.application.schema.camel_case_schema import CamelCaseSchema

class StaffSchema(CamelCaseSchema):
    id = fields.Integer(required=True)
    pension_id = fields.Integer(required=True)
    certification_id = fields.Integer(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    role = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)