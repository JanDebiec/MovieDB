from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

from wtforms.validators import DataRequired


class SingleMovieForm(FlaskForm):
    imdbid = StringField('ImdbId')
    imdbname = StringField('TitleImdb')
    originname = StringField('TitleOrigin')
    localname = StringField('TitleLocal')
    year = StringField('Year')
    director = StringField('Director')
    medium = StringField('Medium')
    place = StringField('Place')
    source = StringField('Source')
    ratingAmg = StringField('AMG rating')
    ownrating = StringField('Ownrating')

class SearchDbForm(SingleMovieForm):
    text = StringField('Text/Title')
    critic = StringField('Critic')
    rating = StringField('rating')
    submit = SubmitField('Search')

class SingleResultForm(SingleMovieForm):
    submit = SubmitField('Submit')


class DeleteMovieForm(SingleMovieForm):
    submit = SubmitField('Delete')

class EditMovieForm(SingleMovieForm):
    submit = SubmitField('Update')

class ExploreForm(FlaskForm):
    localname = StringField('TitleLocal')
    year = StringField('Year')
    director = StringField('Director')

class PageResultsForm(FlaskForm):
    imdbid = StringField('ImdbId')
    localname = StringField('TitleLocal')
    year = StringField('Year')
    director = StringField('Director')
    submit = SubmitField('Update')

class CriticsListForm(FlaskForm):
    submit = SubmitField('Update')

class EditCriticForm(FlaskForm):
    name = StringField('Name')
    url = StringField('Url')
    maxval = StringField('MaxVal')
    submit = SubmitField('Update')

