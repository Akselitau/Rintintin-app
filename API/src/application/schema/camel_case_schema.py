from marshmallow import Schema


class CamelCaseSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = self.camelcase(field_obj.data_key or field_name)

    @staticmethod
    def camelcase(snake_case_string: str):
        parts = iter(snake_case_string.split("_"))
        return next(parts) + "".join(i.title() for i in parts)