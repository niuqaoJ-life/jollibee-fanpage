"""This module contains the forms used in the Jollibee Fanpage website.

The forms in this module are used for user registration,
updating user account information, and changing passwords.
"""

from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User
from werkzeug.security import check_password_hash


class RegistrationForm(FlaskForm):
    """Form class for user registration.

    This form is used to collect user registration information
    such as username, email, and password.
    It also includes validation methods
    to check if the username and email are already taken.

    Attributes:
        username (StringField): Field for entering the username.
        email (StringField): Field for entering the email.
        password (PasswordField): Field for entering the password.
        confirm_password (PasswordField): Field for confirming the password.
        submit (SubmitField): Button for submitting the form.
    Methods:
        validate_username: Validates if the entered username is already taken.
        validate_email: Validates if the entered email is already taken.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter Email Address"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Enter Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Command: Validates the uniqueness of the username.

        Checks if the given username already exists in the database.
        If the username is already taken, raises a ValidationError.

        Parameters:
        - username (str): The username to be validated.

        Raises:
        - ValidationError: If the username is already taken.

        Returns:
        - None
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Command: Validates if the given email is already taken by an existing user.

        Parameters:
            email (str): The email to be validated.
        Raises:
            ValidationError: If the email is already taken by an existing user.
        Returns:
            None
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class UpdateAccountForm(FlaskForm):
    """Form for updating user account information.

    Attributes:
        username (StringField): Field for changing the username.
        email (StringField): Field for changing the email address.
        submit (SubmitField): Button for submitting the form.
    Methods:
        validate_username: Validates the uniqueness of the username.
        validate_email: Validates the uniqueness of the email address.
    """
    username = StringField('Username', validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Change username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
                        "placeholder": "Change email address"})
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validates the username entered in the form.

        Parameters:
        - username (str): The username entered in the form.
        Raises:
        - ValidationError: If the username is already taken.
        Returns:
        - None
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Validates the email input by comparing it with the current user's email and checking if it is already taken by another user.

        Parameters:
        - email (str): The email to be validated.
        Raises:
        - ValidationError: If the email is already taken by another user.
        Returns:
        - None
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class ChangePasswordForm (FlaskForm):
    """Form class for changing user password.

    Attributes:
        old_password (PasswordField): Field for entering the old password.
        new_password (PasswordField): Field for entering the new password.
        confirm_password (PasswordField): Field for confirming the new password.
        submit (SubmitField): Button for submitting the form.
    Methods:
        validate_old_password: Validates the entered old password against the current user's password.
    """
    old_password = PasswordField('Old Password', validators=[
                                 DataRequired()], render_kw={"placeholder": "Old Password"})
    new_password = PasswordField('New Password', validators=[
                                 DataRequired(), Length(min=8)], render_kw={"placeholder": "New Password"})
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(
    ), EqualTo('new_password')], render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField('Change Password')

    def validate_old_password(self, old_password):
        """Validates the old password entered by the user.

        Parameters:
        - old_password (str): The old password entered by the user.
        Raises:
        - ValidationError: If the old password is incorrect.
        """
        user = User.query.filter_by(id=current_user.id).first()
        if user and not check_password_hash(user.password, old_password.data):
            raise ValidationError('Old password is incorrect')
        