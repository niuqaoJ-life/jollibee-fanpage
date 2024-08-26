"""This module defines the database models for the application.

The models include:
- User: Represents a user in the application.
- Post: Represents a post in the application.
- Like: Represents a like given by a user to a post.
- Comment: Represents a comment made by a user on a post.

Each model has its own attributes and relationships with other models.
Note: This module assumes the existence of a Flask application and a database connection.
"""
# Imports necessary modules and functions
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    """Represents a user in the application.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        date_created (datetime): The date and time when the user was created.
        posts (list): The posts created by the user.
        likes (list): The likes given by the user.
        comments (list): The comments made by the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)


class Post(db.Model):
    """Represents a post in the website.

    Attributes:
    - id (int): The unique identifier of the post.
    - text (str): The content of the post.
    - date_created (datetime): The date and time when the post was created.
    - author (int): The ID of the user who created the post.
    - likes (List[Like]): The list of likes received by the post.
    - comments (List[Comment]): The list of comments made on the post.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)


class Like(db.Model):
    """Represents a like on a post.

    Attributes:
        id (int): The unique identifier for the like.
        date_created (datetime): The date and time when the like was created.
        author (int): The ID of the user who created the like.
        post_id (int): The ID of the post that was liked.
    """
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)


class Comment(db.Model):
    """Represents a comment on a post.

    Attributes:
        id (int): The unique identifier for the comment.
        text (str): The content of the comment.
        date_created (datetime): The date and time when the comment was created.
        author (int): The ID of the user who made the comment.
        post_id (int): The ID of the post that the comment belongs to.
    """
    ...
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)
