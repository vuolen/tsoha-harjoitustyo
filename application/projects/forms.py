from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CreateProjectForm(FlaskForm):
    name = StringField("Project name", [validators.Length(min=1)])
    
    class Meta:
        csrf = False

class UpdateProjectForm(FlaskForm):
    name = StringField("Project name", [validators.Length(min=1)])

    class Meta:
        csrf = False
