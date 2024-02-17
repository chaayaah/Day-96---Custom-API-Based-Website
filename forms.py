from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# WTForm for creating a blog post
class CoordinatesForm(FlaskForm):
    lat = StringField("Latitude", validators=[DataRequired()])
    lon = StringField("Longitude", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RandomUserForm(FlaskForm):
    generate = SubmitField("Generate")

class DogsForm(FlaskForm):
    generate = SubmitField("Generate")