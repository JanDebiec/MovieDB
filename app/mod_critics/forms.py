from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

class CompareCriticsForm(FlaskForm):
    critica = StringField('CriticA')
    criticb = StringField('CriticB')
    submit = SubmitField('Compare')

class CompareResultsForm(FlaskForm):
    countA = StringField('Ratings count A')
    countB = StringField('Ratings count B')
    countShared = StringField('Shared Ratings')
    result = StringField('Result')
