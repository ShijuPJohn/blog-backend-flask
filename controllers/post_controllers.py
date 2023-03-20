import uuid

from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage
from marshmallow import ValidationError

from controllers.token_validator import validate_token
from models.models import Post, Category
from serializers.post_serializers import post_create_schema, post_schema, posts_display_schema, category_schema, \
    category_create_schema

post_controller = Blueprint('post_controller', __name__)

db = SQLAlchemy()


@post_controller.route("/api/post", methods=["POST"])
@validate_token
def api_post_create(user_from_token):
    try:
        request_data = request.json
        request_data["author_id"] = user_from_token.id
        categories_from_request = request_data["categories"]
        del (request_data["categories"])
        post_object_from_request = post_create_schema.load(request_data)
        categories_list = Category.query.filter(Category.id.in_(categories_from_request)).all()
        for category in categories_list:
            post_object_from_request.categories.append(category)
        # print(post_object_from_request.categories)
        local_object = db.session.merge(post_object_from_request)
        db.session.add(local_object)
        db.session.commit()
        return {"post": post_schema.dump(post_object_from_request)}, 201

    except ValidationError as v:
        print(v)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/posts", methods=["GET"])
def api_posts_get():
    try:
        posts = Post.query.all()
        return posts_display_schema.dump(posts), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


#
#
@post_controller.route("/api/post/image-upload", methods=["POST"])
@validate_token
def api_post_update_pic(user_from_token):
    try:
        file = request.files["file"]
        client = storage.Client()
        bucket = client.get_bucket('blog-storage1')
        uid = uuid.uuid4()
        blob = bucket.blob(f'{str(uid)[:8]}/{file.name}')
        blob.upload_from_file(file)
        public_url = blob.public_url
        return jsonify({"message": "file_saved", "url": public_url}), 201
    except ValidationError as e:
        print(e)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/category", methods=["POST"])
@validate_token
def api_category_create(user_from_token):
    try:
        request_data = request.json
        print(request_data)
        request_data["author_id"] = user_from_token.id
        category_object_from_request = category_create_schema.load(request_data)
        print(category_object_from_request)
        db.session.add(category_object_from_request)
        db.session.commit()
        return {"category": category_schema.dump(category_object_from_request)}, 201

    except ValidationError as v:
        print(v)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "error"}), 500
