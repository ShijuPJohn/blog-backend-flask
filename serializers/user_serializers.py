import marshmallow as ma
from marshmallow import post_load, fields, validate, Schema

from models.user_models import User


class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    last_name = fields.Str(validate=validate.Length(max=64))
    email = fields.Email(required=True)
    created_time = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
