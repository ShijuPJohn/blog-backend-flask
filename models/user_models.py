import datetime

import flask

# with app.app_context():
#     db = SQLAlchemy(app)
from main import db

print("Has context in", __name__, flask.has_app_context())
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return str(self.id) + "id and name : " + self.first_name
