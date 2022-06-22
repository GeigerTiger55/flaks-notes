from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email


class RegistrationForm(FlaskForm):
    """form to add user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """form for user to login"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class NoteForm(FlaskForm):
    """form to add note"""

    title = StringField("Note Title", validators=[InputRequired()])
    content = TextAreaField("Note:", validators=[InputRequired()])

class CSRFProtectForm(FlaskForm):
    """form just for csrf protection"""
