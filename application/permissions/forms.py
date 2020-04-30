from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, validators
from application.auth.models import User

class AddUserToProjectForm(FlaskForm):
    username = SelectField("Username", choices = [("asd","asdasd"), ("asd1","asd")])
    admin = BooleanField("Admin")
    
    class Meta:
        csrf = False

    def __init__(self, *args, **kw):
        kw["prefix"] = "add_user_to_project"
        super().__init__(*args, **kw)

        project_id = args[0]
        users = User.get_users_not_in_project(project_id)
        self.username.choices = [(user.id, user.username) for user in users]
