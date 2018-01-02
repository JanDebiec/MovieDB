from flask import Blueprint
from flask import flash
from app.userinput import forms as f
from app.db import handler as dbh

# bp = Blueprint('userinput', __name__)

# from app.userinput import handler

# def checkDataFromCsv():
#     '''
#     read CSV file from file system,
#     for every line get the data record,
#     check if movie alredy listed in db
#     and insert/update the db (with the help of db module
#     '''
#     pass
#
# def insertManualInput(manInputForm):
#     ''' extract data from InputForm,
#     validate and insert/update in db
#     '''
#     imdbid = manInputForm.imdbid.data
#     localname = manInputForm.localname.data
#     medium = manInputForm.medium.data
#
#     flash('Added Movie: Id={}, localName={}, medium={}'.format(
#         imdbid, localname, medium
#     ))
#     # dbData = dbh.insertMovieData(imdbid, localname, medium)
#     pass
