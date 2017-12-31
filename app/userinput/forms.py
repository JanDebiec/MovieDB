from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

from wtforms.validators import DataRequired

class ManInputForm(FlaskForm):
    imdbid = StringField('Imdb ID')
    localname = StringField('Localname', validators=[DataRequired()])
    medium = StringField('Medium')
    submit = SubmitField('Submit')

class CsvInputForm(FlaskForm):
    filename = StringField('CsvFileName', validators=[DataRequired()])
    find = SubmitField('find file')
    submit = SubmitField('Submit')