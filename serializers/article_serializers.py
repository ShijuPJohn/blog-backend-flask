from marshmallow import Schema, fields

from serializers.user_serializers import UserSchema


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class ArticleSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    post = fields.String(required=True)
    author = fields.Nested(UserSchema)
    approved_by = fields.Nested(UserSchema)
    category = fields.Nested(CategorySchema, required=True)
    created_time = fields.DateTime()
