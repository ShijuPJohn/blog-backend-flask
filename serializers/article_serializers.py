from marshmallow import Schema, fields

from serializers.user_serializers import UserSchema


class ArticleSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    post = fields.String(required=True)
    author = fields.Nested(UserSchema)
    approved_by = fields.Nested(UserSchema)
    category = fields.Nested(db.ForeignKey(Category.id), nullable=False)
    created_time = fields.DateTime()
