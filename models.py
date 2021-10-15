"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    user_image = db.Column(db.Text, nullable=False)
    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")


class Post(db.Model):
    """Posts model, associated with user"""
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime. now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Tag(db.Model):
    """Tag model, usually assoicated with post"""
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts_table = db.relationship("PostTag", backref="tag")
    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        backref="tags"
    )


class PostTag(db.Model):
    """Model linking post and tags"""
    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
