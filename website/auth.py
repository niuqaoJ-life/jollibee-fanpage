"""Contains the authentication routes and functions for the website.

Routes:
- /login: Handles the login process for users.
Accepts both GET and POST requests.
- /sign-up: Handles the signup process for users.
Accepts both GET and POST requests.
- /logout: Handles the logout process for users.
Requires the user to be logged in.
Functions:
- login(): Handles the login process for users.
Redirects to the home page upon successful login.
- sign_up(): Handles the signup process for users.
Redirects to the login page upon successful signup.
- logout(): Handles the logout process for users.
Redirects to the login page after logging out.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    """Do login process for users.

    If a POST request is received,
    it retrieves the email and password from the request form.
    It then checks if the email exists in the database
    and if the password matches the hashed password stored for that email.
    If the login is successful, the user is logged in,
    a success flash message is displayed,
    and the user is redirected to the home page.
    If the password is incorrect, an error flash message is displayed.
    If the email does not exist, an error flash message is displayed.
    """
    if current_user.is_authenticated:
        flash('You are already logged in.', category='success')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


# Route to authorise user's signup
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    """Sign up route for user registration.

    If the user is already authenticated,
    they will be redirected to the home page.
    Otherwise, the user will be presented with a registration form.
    If the form is submitted and valid,
    the user's account will be created
    and they will be redirected to the login page.

    Returns:
        A redirect response to the home page if the user is already signed in.
        A rendered template for the sign up page with the registration form.
    """
    if current_user.is_authenticated:
        flash('You are already signed in.', category='success')
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            (form.password.data), method='pbkdf2:sha256')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', category='success')
        return redirect(url_for('auth.login'))

    return render_template("signup.html", form=form, user=current_user)


@auth.route("/logout")
@login_required
def logout():
    """Command: Logs out the currently authenticated user.

    Returns:
        A redirect response to the login page.
    Route:
        /logout
    Decorators:
        - @login_required
    Usage:
        Call this function to log out the currently authenticated user
        and redirect to the login page.
    """
    logout_user()
    return redirect(url_for("auth.login"))
