from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

from wtforms.validators import DataRequired

class SearchDbForm(FlaskForm):
    imdbid = StringField('ImdbId')
    text = StringField('Text/Title')
    year = StringField('Year')
    director = StringField('Director')
    submit = SubmitField('Submit')

class SingleResultForm(FlaskForm):
    imdbid = StringField('ImdbId')
    imdbname = StringField('TitleImdb')
    originname = StringField('TitleOrigin')
    localname = StringField('TitleLocal')
    year = StringField('Year')
    director = StringField('Director')
    medium = StringField('Medium')
    source = StringField('Source')

class ExploreForm(FlaskForm):
    localname = StringField('TitleLocal')
    year = StringField('Year')
    director = StringField('Director')
