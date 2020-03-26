from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1)])
    password = PasswordField("Password", [validators.Length(min=6)])
  
    class Meta:
        csrf = False

class RegisterForm(LoginForm):
    fullname = StringField("Full name", [validators.Length(min=1)])
