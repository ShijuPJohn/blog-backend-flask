import uuid

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage
from marshmallow import ValidationError

from controllers.token_validator import validate_token
from models.models import Post, Category
from serializers.post_serializers import post_create_schema, post_schema, posts_display_schema, category_schema, \
    category_create_schema, post_display_schema, categories_minimal_display_schema

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
        title = request_data["title"].lower()
        seo_slug = ""
        if not request_data["seo_slug"]:
            for ch in title:
                if ch.isalnum():
                    seo_slug += ch
                if ch == ' ':
                    seo_slug += '-'
            request_data["seo_slug"] = seo_slug
        if not request_data["meta_description"]:
            request_data["meta_description"] = request_data["description"][:100]
        if user_from_token.admin:
            request_data["approved"] = True
        else:
            request_data["approved"] = False
        post_object_from_request = post_create_schema.load(request_data)
        categories_list = Category.query.filter(Category.id.in_(categories_from_request)).all()
        for category in categories_list:
            post_object_from_request.categories.append(category)
        local_object = db.session.merge(post_object_from_request)
        db.session.add(local_object)
        db.session.commit()
        if user_from_token.admin:
            return {"message": "approved", "post": post_schema.dump(local_object)}, 201
        return {"message": "approval_pending", "post": post_schema.dump(local_object)}, 201

    except ValidationError as v:
        print(v)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/posts", methods=["GET"])
@cross_origin()
def api_posts_get():
    try:
        # posts = Post.query.all()
        posts = Post.query.filter(Post.draft == False, Post.approved == True).all()
        # for post in posts:
        #     post.description=post.description[:100]
        return posts_display_schema.dump(posts), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/user/posts", methods=["GET"])
@validate_token
@cross_origin()
def api_posts_by_user(user_from_token):
    try:
        posts = Post.query.filter(Post.author == user_from_token).all()
        return posts_display_schema.dump(posts), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/posts/<pid>", methods=["PUT"])
@validate_token
@cross_origin()
def api_post_update(pid, user_from_token):
    try:
        data_from_request = request.json
        post = Post.query.filter(Post.id == int(pid)).first()
        current_db_session = db.session.object_session(post)
        if post.author == user_from_token:
            if "title" in data_from_request.keys():
                post.title = data_from_request["title"]
            if "description" in data_from_request.keys():
                post.description = data_from_request["description"]
            if "seo_slug" in data_from_request.keys():
                post.seo_slug = data_from_request["seo_slug"]
            if "draft" in data_from_request.keys():
                post.draft = data_from_request["draft"]
            if "archived" in data_from_request.keys():
                post.archived = data_from_request["archived"]
            if "cover_image" in data_from_request.keys():
                post.cover_image = data_from_request["cover_image"]
            if "categories" in data_from_request.keys():
                categories_from_request = data_from_request["categories"]
                post.categories.clear()
                categories_list = Category.query.filter(Category.id.in_(categories_from_request)).all()
                post.categories += categories_list
            if "meta_description" in data_from_request.keys():
                post.meta_description = data_from_request["meta_description"]
            current_db_session.add(post)
            current_db_session.commit()
            return {"message": "post_updated", "post": post_schema.dump(post)}, 201
        return jsonify({"message": "unauthorized"}), 401
    except Exception as e:
        print(e)
        return {"message": "error"}, 500


@post_controller.route("/api/posts/<pid>", methods=["DELETE"])
@validate_token
@cross_origin()
def api_posts_delete(user_from_token, pid):
    try:
        post = Post.query.filter(Post.id == pid).first()
        if not post:
            return jsonify({"message": "not_found"}), 404
        print(post.author)
        print(user_from_token)
        if post.author == user_from_token:
            local_object = db.session.merge(post)
            db.session.delete(local_object)
            db.session.commit()
            return jsonify({"message": "deleted"}), 200
        return jsonify({"message": "unauthorized"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/post/<pid>", methods=["GET"])
@cross_origin()
def api_post_get(pid):
    try:
        post = Post.query.filter(Post.id == pid).first()
        if post:
            return post_display_schema.dump(post), 200
        return jsonify({"message": "not_found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/post/byslug/<slug>", methods=["GET"])
@cross_origin()
def api_post_getbyslug(slug):
    try:
        post = Post.query.filter(Post.seo_slug == slug).first()
        if not post:
            return jsonify({"message": "not_found"}), 404
        return post_display_schema.dump(post), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/post/image-upload", methods=["POST"])
@validate_token
@cross_origin()
def api_post_update_pic(user_from_token):
    try:
        file = request.files["file"]
        client = storage.Client()
        bucket = client.get_bucket('blog-storage1')
        uid = uuid.uuid4()
        blob = bucket.blob(f'{str(uid)[:8]}/{file.filename}')
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
        request_data["author_id"] = user_from_token.id
        category_object_from_request = category_create_schema.load(request_data)
        db.session.add(category_object_from_request)
        db.session.commit()
        return {"category": category_schema.dump(category_object_from_request)}, 201

    except ValidationError as v:
        print(v)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "error"}), 500


@post_controller.route("/api/categories", methods=["GET"])
@validate_token
def api_categories_get(user_from_token):
    try:
        categories = Category.query.all()
        return categories_minimal_display_schema.dump(categories), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500
