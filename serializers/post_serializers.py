from flask_marshmallow import Marshmallow
from marshmallow import post_load

from models.models import Post
from serializers.user_serializers import UserDisplaySchema

ma = Marshmallow()


class PostSchema(ma.Schema):
    class Meta:
        model = Post
        fields = ("id", "title", "description", "imageUrl", "time_created", "author", "archived")

    # author = ma.Nested(UserDisplaySchema)


class PostCreateSchema(ma.Schema):
    class Meta:
        model = Post
        fields = ("title", "description", "author_id")

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
post_create_schema = PostCreateSchema()
