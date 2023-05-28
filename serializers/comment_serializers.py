from flask_marshmallow import Marshmallow
from marshmallow import post_load
from marshmallow_sqlalchemy import fields

from models.models import Comment, GuestComment, BlogMessage, PortfolioMessage
from serializers.user_serializers import user_display_schema, user_minimal_display_schema, users_minimal_display_schema

ma = Marshmallow()


class GuestCommentSchema(ma.Schema):
    class Meta:
        model = GuestComment
        fields = (
            "id", "comment", "author_name", "author_email", "post_id", "time_created", "liked_users", "guest_likes")

    liked_users = fields.Nested(users_minimal_display_schema)

    @post_load
    def make_guest_comment(self, data, **kwargs):
        return GuestComment(**data)


class GuestCommentDisplaySchema(ma.Schema):
    class Meta:
        model = GuestComment
        fields = (
            "id", "comment", "author_name", "author_email", "post_id", "time_created","time_updated", "liked_users", "guest_likes")

    liked_users = fields.Nested(users_minimal_display_schema)


guest_comment_schema = GuestCommentSchema()
guest_comment_display_schema = GuestCommentDisplaySchema()
guest_comments_display_schema = GuestCommentDisplaySchema(many=True)
