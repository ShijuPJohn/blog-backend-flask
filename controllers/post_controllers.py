# import os
#
# from flask import Blueprint, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from marshmallow import ValidationError
# from werkzeug.utils import secure_filename
#
# from controllers.token_validator import validate_token
# from models.models import Post
# from serializers.post_serializers import post_create_schema, post_schema
#
# post_controller = Blueprint('post_controller', __name__)
#
# db = SQLAlchemy()
#
#
# @post_controller.route("/api/post", methods=["POST"])
# @validate_token
# def api_post_create(user_from_token):
#     try:
#         request_data = request.json
#         request_data["author_id"] = user_from_token.id
#         post_object_from_request = post_create_schema.load(request_data)
#         db.session.add(post_object_from_request)
#         db.session.commit()
#         return {"post": post_schema.dump(post_object_from_request)}, 200
#
#     except ValidationError as v:
#         print(v)
#         return jsonify({"message": "bad_request"}), 400
#     except Exception as e:
#         print("Exception", e)
#         return jsonify({"message": "error"}), 500
#
#
# @post_controller.route("/api/post/image-upload", methods=["POST"])
# @validate_token
# def api_post_update_pic(pid, user_from_token):
#     try:
#         post = Post.query.filter(Post.id == int(pid)).first()
#         if post.author == user_from_token:
#             file = request.files["file"]
#             file_ext = file.filename[file.filename.rfind('.'):]
#             s_fname = secure_filename(pid + file_ext)
#             file.save(os.path.join(app.config['UPLOADS_DIR'] + "post_thumbs", s_fname))
#             post.imageUrl = os.path.join(app.config['UPLOADS_DIR'] + "post_thumbs", s_fname)
#             db.session.add(post)
#             db.session.commit()
#             return jsonify({"message": "file_saved"}), 201
#         return jsonify({"message": "unauthorized"}), 401
#     except ValidationError as e:
#         print(e)
#         return jsonify({"message": "bad_request"}), 400
#     except Exception as e:
#         print(e)
#         return jsonify({"message": "error"}), 500
