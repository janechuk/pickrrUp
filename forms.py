from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Optional, NumberRange, Length, Email


class RegisterUserForm(FlaskForm):
    """Form for registering user for feedback app."""
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=30, message=None)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=1, max=30, message=None)])
    email = StringField("Email", validators=[
                        InputRequired(), Email(), Length(max=50, message=None)])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=50)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=50)])


class LogInUserForm(FlaskForm):
    """ Form for loging In """
    username = StringField("Username", validators=[
        InputRequired(), Length(min=1, max=30, message=None)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6, max=30, message=None)])