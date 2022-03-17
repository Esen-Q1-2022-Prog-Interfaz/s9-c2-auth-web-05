from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length


class TaskUpdateForm(FlaskForm):
    description = StringField(
        validators=[
            InputRequired(),
            Length(min=1, max=200),
        ],
        render_kw={"placeholder": "description"},
    )

    status = SelectField(
        "status",
        choices=[("new", "New"), ("in progress", "In progress"), ("done", "Done")],
        validators=[InputRequired()],
    )

    submit = SubmitField("update task")
