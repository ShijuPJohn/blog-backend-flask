from flask import request, current_app as app
from flask_sqlalchemy import SQLAlchemy

from models.user_models import User
from serializers.user_serializers import users_schema, user_schema, user_signup_schema

db = SQLAlchemy(app)


# with app.app_context():
#     db = SQLAlchemy(app)


@app.route('/api/users', methods=["POST"])
def user_post():
    data = request.json
    user_object = user_signup_schema.load(data)
    db.session.add(user_object)
    db.session.commit()
    return user_schema.dump(user_object)


@app.route('/api/users', methods=["GET"])
def users_get():
    users = User.query.all()
    return users_schema.dump(users)
