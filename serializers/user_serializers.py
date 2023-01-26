from flask_marshmallow import Marshmallow
from marshmallow import post_load, Schema

from main import app
from models.user_models import User

ma = Marshmallow(app)


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_time']


class UserSignupSchema(Schema):
    class Meta:
        model = User
        fields = [ 'username', 'email']

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_signup_schema = UserSignupSchema()
