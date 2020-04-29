from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

from application.auth.models import User
  
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1, max=20)])
    password = PasswordField("Password", [validators.Length(min=6, max=100)])
  
    class Meta:
        csrf = False

class RegisterForm(LoginForm):
    fullname = StringField("Full name", [validators.Length(min=1, max=100)])

    def validate_username(form, field):
        if User.username_exists(field.data):
            print("USERNAME EXISTS")
            raise ValidationError("Username already exists")
