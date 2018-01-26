from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

class CompareCriticsForm(FlaskForm):
    critica = StringField('CriticA')
    criticb = StringField('CriticB')
    submit = SubmitField('Compare')

class CompareResultsForm(FlaskForm):
    critica = StringField('CriticA')
    criticb = StringField('CriticB')
    countA = StringField('Ratings A count')
    countB = StringField('Ratings B count')
    countShared = StringField('Shared Ratings')
    result = StringField('Result')
