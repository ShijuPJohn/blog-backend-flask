import datetime

from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

from models.user_models import User

with app.app_context():
    db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Category with name : " + self.name


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post = db.Column(db.Text, nullable=False)
    author = db.Column(db.ForeignKey(User.id), nullable=False)
    category = db.Column(db.ForeignKey(Category.id), nullable=False)
    approved_by = db.Column(db.ForeignKey(User.id), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __str__(self):
        return "Article with title : ", str(self.title) + ". Created at : " + self.created_time
