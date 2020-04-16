from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CreateStageForm(FlaskForm):
    name = StringField("Stage name", [validators.Length(min=1)])

    class Meta:
        csrf = False
