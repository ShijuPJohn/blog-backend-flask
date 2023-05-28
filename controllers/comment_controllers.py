import uuid

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from controllers.token_validator import validate_token
from models.models import Post, Category
from serializers.comment_serializers import guest_comment_schema, guest_comment_display_schema, \
    guest_comments_display_schema

comment_controller = Blueprint('comment_controller', __name__)

db = SQLAlchemy()


@comment_controller.route("/api/comment", methods=["POST"])
def api_guest_comment_create():
    try:
        request_data = request.json
        comment_object_from_request = guest_comment_schema.load(request_data)
        print(comment_object_from_request)
        local_object = db.session.merge(comment_object_from_request)
        db.session.add(local_object)
        db.session.commit()
        return jsonify(
            {'message': 'test working', 'comment': guest_comment_display_schema.dump(local_object)}), 201
    except ValidationError as ve:
        return jsonify({'message': 'validation error'}), 500
    except Exception as e:
        print(e)
        return jsonify({'message': 'server error'}), 500


@comment_controller.route("/api/comment_by_pid/<pid>", methods=["GET"])
def api_guest_comment_get_by_postid(pid):
    try:
        post = Post.query.filter(Post.id == pid).first()
        if not post:
            return jsonify({'message': 'not found'}), 404
        print(post)
        print(post.guest_comments)
        return guest_comments_display_schema.dump(post.guest_comments), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'server error'}), 500
