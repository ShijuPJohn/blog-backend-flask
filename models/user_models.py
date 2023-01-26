import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

# with app.app_context():
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "n_user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __str__(self):
        return self.username
