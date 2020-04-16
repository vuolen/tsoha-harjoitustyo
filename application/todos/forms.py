from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class CreateTodoForm(FlaskForm):
    text = TextAreaField("text", [validators.Length(min=1, max=1000)])

    class Meta:
        csrf = False
