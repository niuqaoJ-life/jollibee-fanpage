# Imports necessary modules and functions
from . import db # Imports  database instance from the current package 
from flask_login import UserMixin # Imports UserMixin to manage user session
from sqlalchemy.sql import func # Imports func for SQL database functions

# Defines User model, inheriting from db.Model and UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Primary key for the User table of database
    email = db.Column(db.String(150), unique=True) # Email field, must be unique, string limit of 150 letters
    username = db.Column(db.String(150), unique=True) # Username field, must be unique, string limit of 150 letters
    password = db.Column(db.String(150)) # Password field, string limit of 150 letters
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) #Timestamp for when user creates their account
    posts = db.relationship('Post', backref='user', passive_deletes=True) # Relationship with posts table
    likes = db.relationship('Like', backref='user', passive_deletes=True) # User table relationship with likes table 
    comments = db.relationship('Comment', backref='user', passive_deletes=True) # User table has relationship with comments table

# Defines the post model of the database, inherits from db.Model    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key for the post table
    text = db.Column(db.Text, nullable=False) # Text field when creating post, cannot be null
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) #timepstamp for when post is created 
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # Foreign key to User table with cascade on delete
    likes = db.relationship('Like', backref='post', passive_deletes=True) #Creates link/relationship with like table, with passive deletes
    comments = db.relationship('Comment', backref='post', passive_deletes=True) # Creates link/relationship with comments table, with passive deletes 
    
# Defines the like table model of the database, inherits from db.Model    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key for like table
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # Timestamp when user likes post
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # Foreign key to User table with cascade on delete
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False) # Foreign key to Post table with cascade on delete

# Defines the comment table of the database, inherits from db.Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key for the comment table
    text = db.Column(db.Text, nullable=False) # Text field for the comment content, cannot be null/empty
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # Timestamp for when user comments on post
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # Foreign key to User table with cascade on delete
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False) # Foreign key to Post table with cascade on delete