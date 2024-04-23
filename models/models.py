import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func

db = SQLAlchemy()

follows_followedby = db.Table("follows_followedby",
                              db.Column("user", db.Integer, db.ForeignKey("user1.id")),
                              db.Column("follows", db.Integer, db.ForeignKey("user1.id"))
                              )
post_likes = db.Table("post_likes",
                      db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
                      db.Column("user_id", db.Integer, db.ForeignKey("user1.id"))
                      )
comment_likes = db.Table("comment_likes",
                         db.Column("post_id", db.Integer, db.ForeignKey("comment.id")),
                         db.Column("user_id", db.Integer, db.ForeignKey("user1.id"))
                         )
guest_comment_likes = db.Table("guest_comment_likes",
                               db.Column("post_id", db.Integer, db.ForeignKey("guest_comment.id")),
                               db.Column("user_id", db.Integer, db.ForeignKey("user1.id"))
                               )

post_categories = db.Table("post_categories",
                           db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
                           db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
                           )


class User(db.Model):
    __tablename__ = "user1"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    profile_image = db.Column(db.String, nullable=True, default="")  # TODO default=?
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    follows = db.relationship("User", secondary=follows_followedby,
                              primaryjoin=follows_followedby.c.user == id,
                              secondaryjoin=follows_followedby.c.follows == id,
                              backref="followers")
    posts = db.relationship("Post", backref="author")
    created_categories = db.relationship("Category", backref="created_by")
    comments = db.relationship("Comment", cascade="all,delete", backref="author")
    liked_posts = db.relationship("Post", secondary=post_likes, backref="liked_users")
    liked_comments = db.relationship("Comment", secondary=comment_likes, backref="liked_users")
    liked_guest_comments = db.relationship("GuestComment", secondary=guest_comment_likes, backref="liked_users")
    about = db.Column(db.String, nullable=True, default='')
    linkedin_url = db.Column(db.String, nullable=True, default='')
    github_url = db.Column(db.String, nullable=True, default='')
    portfolio_url = db.Column(db.String, nullable=True, default='')

    def __str__(self):
        return "User object" + self.email


class Comment(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user1.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    guest_likes = db.Column(db.Integer, default=0)

    def __str__(self):
        return "Comment with content: " + self.comment


class GuestComment(db.Model):
    __tablename__ = "guest_comment"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    author_name = db.Column(db.String, nullable=False)
    author_email = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    guest_likes = db.Column(db.Integer, default=0)

    def __str__(self):
        return "Guest comment with content: " + self.comment


class Post(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    seo_slug = db.Column(db.String, unique=True)
    description = db.Column(db.String, nullable=True)
    meta_description = db.Column(db.String, nullable=True)
    cover_image = db.Column(db.String, nullable=True)  # TODO default=?
    cover_video = db.Column(db.String, nullable=True)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey("user1.id"), nullable=False)
    comments = db.relationship("Comment", cascade="all,delete", backref="Post", order_by='Comment.time_created.desc()')
    guest_comments = db.relationship("GuestComment", cascade="all,delete", backref="Post",
                                     order_by='GuestComment.time_created.desc()')
    archived = db.Column(db.Boolean, default=False, nullable=False)
    approved = db.Column(db.Boolean, default=False, nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    categories = db.relationship("Category", secondary=post_categories, backref="posts")
    guest_likes = db.Column(db.Integer, default=0)

    def __str__(self):
        return "Post with title : " + self.title


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user1.id"), nullable=True)

    def __str__(self):
        return "Category with name : " + self.name


class BlogMessage(db.Model):
    __tablename__ = "blog_message"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

    def __str__(self):
        return "Blog Contact Message with name : " + self.name


class PortfolioMessage(db.Model):
    __tablename__ = "portfolio_message"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

    def __str__(self):
        return "Portfolio Contact Message with name : " + self.name
