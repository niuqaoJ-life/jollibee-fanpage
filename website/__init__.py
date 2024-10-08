"""Initializes the Flask application and configures with necessary modules etc.

Functions:
- create_app(): Creates and configures the Flask app,
initializes the database, registers blueprints,
and sets up user authentication.
"""

# Importing necessary modules from flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Creates an SQLAlchemy object for the database
db = SQLAlchemy()
DB_NAME = "database.db"


# Function creates the flask app and configures it
def create_app():
    """Create and configures the Flask application.

    Returns:
        app (Flask): The configured Flask application.
    Raises:
        None
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "7QmMbkyHfp"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Imports and register the blueprints for parts website
    # imports views blueprints from python file
    # imports auth blueprints from python file
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # From models python file, takes user and the post.
    from .models import User

    # Creates tables in the database if not existing
    with app.app_context():
        db.create_all()

    # Login manager for user authentification.
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Defines user loader callback for the login manager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
