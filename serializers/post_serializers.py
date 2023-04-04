from flask_marshmallow import Marshmallow
from marshmallow import post_load
from marshmallow_sqlalchemy import fields

from models.models import Post, Category
from serializers.user_serializers import user_display_schema, user_minimal_display_schema

ma = Marshmallow()


class CategorySchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("id", "name", "created_by")

    created_by = fields.Nested(user_minimal_display_schema)


categories_schema = CategorySchema(many=True)


class CategoryMinimalSchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("id", "name")


categories_minimal_schema = CategoryMinimalSchema(many=True)


class PostSchema(ma.Schema):
    class Meta:
        model = Post
        fields = (
            "id", "title", "description", "cover_image", "time_created", "author", "archived", "draft", "categories",
            "author", "seo_slug")

    author = fields.Nested(user_display_schema)
    categories = fields.Nested(categories_minimal_schema)
    # author = ma.Nested(UserDisplaySchema)


class PostCreateSchema(ma.Schema):
    class Meta:
        model = Post
        fields = ("title", "description", "author_id", "archived", "seo_slug", "cover_image", "draft")

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)


class PostDisplaySchema(ma.Schema):
    class Meta:
        model = Post
        fields = (
            "id", "title", "description", "author", "archived", "cover_image", "draft", "categories", "time_created",
            "seo_slug")

    author = fields.Nested(user_display_schema)
    categories = fields.Nested(categories_minimal_schema)


class CategoryCreateSchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("name", "author_id")

    @post_load
    def make_category(self, data, **kwargs):
        return Category(**data)


class CategoryMinimalDisplaySchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("name", "id")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
posts_display_schema = PostDisplaySchema(many=True)
post_display_schema = PostDisplaySchema()
post_create_schema = PostCreateSchema()
category_schema = CategorySchema()
category_create_schema = CategoryCreateSchema()
categories_minimal_display_schema = CategoryMinimalDisplaySchema(many=True)
