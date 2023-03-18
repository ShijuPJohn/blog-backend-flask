import datetime

import jwt
from flask import request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

import config
# from controllers.token_validator import validate_token
from models.models import User
from serializers.user_serializers import users_display_schema, user_signup_schema, user_display_schema

db = SQLAlchemy()

user_controller = Blueprint('user_controller', __name__)


@user_controller.route("/api/users", methods=["GET"])
# @validate_token
def api_users_get():
    try:
        users = User.query.all()
        return users_display_schema.dump(users), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@user_controller.route("/api/users", methods=["POST"])
def api_user_signup():
    try:
        user_from_request = request.json
        user = user_signup_schema.load(user_from_request)
        if user:
            hashed_password = generate_password_hash(user.password, method="sha256")
            user.password = hashed_password
            db.session.add(user)
            db.session.commit()
            # token = jwt.encode(
            #     {"user_id": user.id,
            #      "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)},
            #     config.secret_key
            # )
            return {"user": user_display_schema.dump(user)}
                # , "token": token}
    except ValidationError:
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "internal_server_error"}), 500

#
# @app.route("/api/user", methods=["PUT"])
# @validate_token
# def api_user_update(user_from_token):
#     try:
#         data_from_request = request.json
#         if check_password_hash(user_from_token.password, data_from_request["password"]):
#             user_from_token.username = data_from_request["username"]
#             user_from_token.password = generate_password_hash(data_from_request["password"], method="sha256")
#             db.session.add(user_from_token)
#             db.session.commit()
#             return {"message": "user_updated"}, 201
#         return {"message": "unauthorized"}, 401
#
#     except Exception as e:
#         print(e)
#         return {"message": "error"}, 500
#
#
# @app.route("/api/user", methods=["DELETE"])
# @validate_token
# def api_user_delete(user_from_token):
#     try:
#         data_from_request = request.json
#         if check_password_hash(user_from_token.password, data_from_request["password"]):
#             db.session.delete(user_from_token)
#             db.session.commit()
#             return {"message": "user_deleted"}, 200
#     except Exception as e:
#         print(e)
#         return {"message": "error"}, 500
#
#
# @app.route("/api/user/profile-pic", methods=["PUT"])
# @validate_token
# def api_user_prof_pic(user_from_token):
#     try:
#         file = request.files["file"]
#         file_ext = file.filename[file.filename.rfind('.'):]
#         s_fname = secure_filename(str(user_from_token.id) + file_ext)
#         file.save(os.path.join(app.config['UPLOADS_DIR'] + "user_thumbs", s_fname))
#         user_from_token.imageUrl = os.path.join(app.config['UPLOADS_DIR'] + "user_thumbs", s_fname)
#         db.session.add(user_from_token)
#         db.session.commit()
#         return jsonify({"message": "file_saved"})
#     except Exception as e:
#         print(e)
#         return jsonify({"message": "bad_request"}), 400
#
#
# @user_controller.route('/api/user/login', methods=["POST"])
# def api_user_login():
#     body_data = request.get_json()
#     if body_data["email"] and body_data["password"]:
#         email_from_request = body_data["email"]
#         password_from_request = body_data["password"]
#         user = User.query.filter(User.email == email_from_request).first()
#         if user and check_password_hash(user.password, password_from_request):
#             token = jwt.encode(
#                 {"user_id": user.id,
#                  "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)},
#                 config.secret_key
#             )
#             return jsonify({"message": "login_success", "token": token}), 200
#         return {"message": "invalid_credentials"}, 401
#     return {"message": "invalid_data"}, 400
#
#
# @app.route('/api/user/<uid>', methods=["GET"])
# @validate_token
# def api_user_get(uid, user_from_token):
#     requested_user = User.query.filter(User.id == int(uid)).first()
#     if requested_user:
#         return user_display_schema.jsonify(requested_user)
#     return {"status": "not_found"}, 404
#
#
# @app.route('/api/user/follow-unfollow/<uid>', methods=["POST"])
# @validate_token
# def api_user_follow_unfollow(uid, user_from_token):
#     try:
#         user_to_follow_or_unfollow = User.query.filter(User.id == uid).first()
#         if user_to_follow_or_unfollow:
#             if user_to_follow_or_unfollow in user_from_token.follows:
#                 user_from_token.follows.remove(user_to_follow_or_unfollow)
#                 db.session.add(user_from_token)
#                 db.session.commit()
#                 return {"message": "unfollowed"}, 200
#             else:
#                 user_from_token.follows.append(user_to_follow_or_unfollow)
#                 db.session.add(user_from_token)
#                 db.session.commit()
#                 return {"status": "followed"}
#         return {"status": "not_found"}, 404
#     except Exception as e:
#         print(e)
#         return {"message": "error"}, 500
#
