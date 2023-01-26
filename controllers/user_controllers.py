from flask import request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models.user_models import User
from serializers.user_serializers import users_schema, user_schema, user_signup_schema

db = SQLAlchemy()

user_controllers = Blueprint('user_controllers', __name__)


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
    return users_schema.dump(users)
