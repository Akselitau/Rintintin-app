from marshmallow import fields
from chalicelib.application.schema.camel_case_schema import CamelCaseSchema

class CertificationSchema(CamelCaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    validity = fields.String(required=True)
