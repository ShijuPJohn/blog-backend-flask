import marshmallow as ma
from marshmallow import post_load

from models.user_models import User


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'created_time')

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
