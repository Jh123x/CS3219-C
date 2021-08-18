from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)], render_kw={"class": "form-control"})
    password = PasswordField('Password', [validators.DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember me', render_kw={"class": "form-check-input"})


class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)], render_kw={"class": "form-control"})
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={"class": "form-control"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"class": "form-control"})
    confirm = PasswordField('Repeat Password', render_kw={"class": "form-control"})
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()], render_kw={"class": "form-check-input"})