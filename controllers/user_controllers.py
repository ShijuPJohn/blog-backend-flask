from flask import request, jsonify, current_app as app
from flask_sqlalchemy import SQLAlchemy
from models.user_models import User
from serializers.user_serializers import users_schema, user_schema
with app.app_context():
    db = SQLAlchemy(app)


@app.route('/user', methods=["POST"])
def user_post():
    data = request.json
    user_object = user_schema.load(data)
    db.session.add(user_object)
    db.session.commit()
    return jsonify(user_schema.dump(user_object))


@app.route('/users', methods=["GET"])
def users_get():
    users = User.query.all()
    results = users_schema.dump(users)
    return jsonify(results)
