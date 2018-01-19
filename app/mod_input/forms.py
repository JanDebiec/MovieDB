from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

from wtforms.validators import DataRequired

# class ManInputForm(FlaskForm):
#     imdbid = StringField('Imdb ID')
#     localname = StringField('Localname')
#     medium = StringField('Medium')
#     submit = SubmitField('Submit')
#
class ManInputForm(FlaskForm):
    imdbid = StringField('Imdb ID')
    imdbname = StringField('ImdbName')
    originname = StringField('OriginalName')
    localname = StringField('LocalName')
    medium = StringField('Medium')
    place = StringField('Place')
    source = StringField('Source')
    ownrating = StringField('MyOwnRating')
    submit = SubmitField('Submit')

class CsvInputForm(FlaskForm):
    filename = StringField('CsvFileName', validators=[DataRequired()])
    find = SubmitField('find file')
    submit = SubmitField('Submit')