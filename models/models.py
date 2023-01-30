import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func

db = SQLAlchemy()

follows_followedby = db.Table("follows_followedby",
                              db.Column("user", db.Integer, db.ForeignKey("user.id")),
                              db.Column("follows", db.Integer, db.ForeignKey("user.id"))
                              )
post_likes = db.Table("post_likes",
                      db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
                      db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                      )
comment_likes = db.Table("comment_likes",
                         db.Column("post_id", db.Integer, db.ForeignKey("comment.id")),
                         db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                         )

post_categories = db.Table("post_categories",
                           db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
                           db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
                           )#TODO

post_authors = db.Table("post_authors",
                           db.Column("post_id", db.Integer, db.ForeignKey("user.id")),
                           db.Column("category_id", db.Integer, db.ForeignKey("post.id"))
                           )#TODO

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)
    profile_image = db.Column(db.String, nullable=True, default="static/uploads/user_thumbs/pro_img1.png")
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    follows = db.relationship("User", secondary=follows_followedby,
                              primaryjoin=follows_followedby.c.user == id,
                              secondaryjoin=follows_followedby.c.follows == id,
                              backref="followers")
    posts = db.relationship("Post", cascade="all,delete", backref="author", order_by='Post.time_created.desc()')  # TODO
    categories = db.relationship("Category", cascade="all,delete", backref="author",
                                 order_by='Post.time_created.desc()')  # TODO
    comments = db.relationship("Comment", cascade="all,delete", backref="author")  # TODO
    liked_posts = db.relationship("Post", secondary=post_likes, backref="liked_users")  # TODO
    liked_comments = db.relationship("Comment", secondary=comment_likes, backref="liked_users")  # TODO

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return "User object" + self.email


class Comment(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

    def __str__(self):
        return "Comment with content: " + self.comment


class Post(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    cover_image = db.Column(db.String, nullable=True, default="static/uploads/post_thumbs/default_post.png")
    cover_video = db.Column(db.String, nullable=True)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", cascade="all,delete", backref="Post", order_by='Comment.time_created.desc()')
    archived = db.Column(db.Boolean, default=False, nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)

    def __str__(self):
        return "Post with title : " + self.title


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Category with name : " + self.name
