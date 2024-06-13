from marshmallow import Schema, fields

class ReservationSchema(Schema):
    reservation_id = fields.Int(required=True)
    dog_id = fields.Int(required=True)
    pension_id = fields.Int(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    status = fields.Str(required=True)
