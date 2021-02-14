from marshmallow import Schema, fields


class User(Schema):
    id = fields.Integer()
    u_id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
