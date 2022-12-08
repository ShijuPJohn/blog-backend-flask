from flask import current_app as app, request, jsonify

from main import db
from models.article_models import Article
from serializers.article_serializers import article_schema, category_schema


@app.route("/article", methods=["POST"])
def article_post():
    data = request.json
    art_object = article_schema.load(data)
    db.session.add(art_object)
    db.session.commit()
    return jsonify(article_schema.dump(art_object))


@app.route("/article/<art_id>", methods=["GET"])
def article_get(art_id):
    article = Article.query.filter(Article.id == art_id).first()
    article_json = article_schema.dump(article)
    return jsonify(article_json)


@app.route("/category", methods=["POST"])
def category_post():
    data = request.json
    category_object = category_schema.load(data)
    db.session.add(category_object)
    db.session.commit()
    return jsonify(category_schema.dump(category_object))
