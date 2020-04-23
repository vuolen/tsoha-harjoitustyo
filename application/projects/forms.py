from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, validators

class CreateProjectForm(FlaskForm):
    name = StringField("Project name", [validators.Length(min=1, max=30)])
    
    class Meta:
        csrf = False

class UpdateProjectForm(FlaskForm):
    name = StringField("Project name", [validators.Length(min=1, max=30)])

    class Meta:
        csrf = False

    def __init__(self, *args, **kw):
        kw["prefix"] = "update_project"
        super().__init__(*args, **kw)
