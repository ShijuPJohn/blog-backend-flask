import jwt
from flask import request, Blueprint, jsonify, current_app as app
from flask_sqlalchemy import SQLAlchemy

import config
from models.models import User
from serializers.user_serializers import users_display_schema, user_schema, user_signup_schema

db = SQLAlchemy()

user_controllers = Blueprint('user_controllers', __name__)

def validate_token(func):
    def w_func(*args, **kwargs):
        token = None
        if "x-token" in request.headers:
            token = request.headers["x-token"]
        if not token:
            return jsonify({"message": "token_absent"}), 401
        try:
            decoded_data = jwt.decode(token, config.secret_key, algorithms=['HS256'])
            user_id_from_token = decoded_data["user_id"]
            user = User.query.filter(User.id == user_id_from_token).first()
            kwargs["user_from_token"] = user
            val = func(*args, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({"message": "invalid_token"}), 401
        return val

    w_func.__name__ = func.__name__

    return w_func


@user_controllers.route('/api/users', methods=["POST"])
def user_post():
    data = request.json
    user_object = user_signup_schema.load(data)
    db.session.add(user_object)
    db.session.commit()
    return user_schema.dump(user_object)


@user_controllers.route('/api/users', methods=["GET"])
def users_get():
    users = User.query.all()
    return users_display_schema.dump(users)
