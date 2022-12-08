from marshmallow import Schema, fields, post_load

from models.article_models import Article, Category
from serializers.user_serializers import UserSchema


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

    @post_load
    def make_category(self, data, **kwargs):
        return Category(**data)


class ArticleSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    post = fields.String(required=True)
    author = fields.Integer()
    approved_by = fields.Integer()
    category = fields.Integer(required=True)
    created_time = fields.DateTime()

    @post_load
    def make_article(self, data, **kwargs):
        print(data, kwargs)
        return Article(**data)


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
