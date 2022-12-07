from flask import request, jsonify

from main import app, db
from models.user_models import User
from serializers.user_serializers import users_schema


@app.route('/user', methods=["POST"])
def user_post():
    data = request.json
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    user = User(first_name, last_name, email)
    db.session.add(user)
    db.session.commit()
    return str(user.id)


@app.route('/users', methods=["GET"])
def users_get():
    users = User.query.all()
    results = users_schema.dump(users)
    return jsonify(results)
