from flask import Blueprint, render_template, flash, redirect, url_for
import csv

from config import Config

import helper as h
import app.mod_imdb.controllers as tsv

from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic

from app.mod_input.forms import  CsvInputForm
import app.mod_db.functions as dbc

mod_input = Blueprint('input', __name__, url_prefix='/mod_input')

# @mod_input.route('/maninput', methods=['GET', 'POST'])
# def maninput():
#     form = ManInputForm()
#     if form.validate_on_submit():
#         flash('Added Movie: Id={}, localName={}, medium={}'.format(
#             form.imdbid.data, form.localname.data, form.medium.data
#         ))
#         insertManualInput(form)
#         return redirect('/index')
#     return render_template('mod_input/maninput.html',
#                            title='Manual Input',
#                            form=form)
#
#

@mod_input.route('/csvinput', methods=['GET', 'POST'])
def csvinput():
    form = CsvInputForm()
    if form.validate_on_submit():
        flash('File choosen: {}'.format(
            form.filename.data
        ))
        ownerName = Config.OWNER_NAME
        owner = Critic(name=ownerName, maxVal='5.0')
        amg = Critic(name='AMG', maxVal='5.0')
        mc = Critic(name='MC', url='http://www.metacritic.com/', maxVal='100.0')
        imdb = Critic(name='Imdb', maxVal='10.0')
        db.session.add(owner)
        db.session.add(imdb)
        db.session.add(amg)
        db.session.add(mc)
        db.session.commit()

        fileName = '/home/jan/project/movie_db/userdata/input.csv'
        # fileName = '/home/jan/project/movie_db/userdata/input_80.csv'
        readFileAddItemsToDb(fileName)
        # readFileAddItemsToDb(form.filename.data)
        return redirect('/index')
    return render_template('mod_input/csvinput.html',
                           title='CSV Input',
                           form=form)

def checkDataFromCsv():
    '''
    read CSV file from file system,bbb
    for every line get the data record,
    check if movie alredy listed in db
    and insert/update the db (with the help of db module
    '''
    pass

# def insertManualInput(manInputForm):
#     ''' extract data from InputForm,
#     validate and insert/update in db
#     '''
#     imdbid = manInputForm.imdbid.data
#     localname = manInputForm.localname.data
#     medium = manInputForm.medium.data
#     place = manInputForm.place.data
#     ownrating = manInputForm.ownrating.data
#     amgrating = manInputForm.amgrating.data
#
#     flash('Added Movie: Id={}, localName={}, medium={}'.format(
#         imdbid, localname, medium
#     ))
#     dbc.insertMovieData(inputMovieId=imdbid,
#                         inputTitle=localname,
#                         medium=medium,
#                         place=place,
#                         ownrating=ownrating,
#                         amgrating=amgrating)
#
def readFileAddItemsToDb(fileName):
    with h.ManagedUtfFile(fileName) as f:
        csvReader = csv.reader(f)
        count = 0
        data = False
        for row in csvReader:
            if data == False:
                data = True
            else:
                if len(row) > 0:
                    count = count + 1
                    imdbID = row[0]
                    # only rows with not empty and zero imdbId
                    # if imdbID != '' and imdbID != '0000000':
                    if len(row) > 4:
                        titlelocal = row[4]
                    else:
                        titlelocal = ''
                    if len(row) > 5:
                        medium = row[5]
                        if medium == '':
                            medium = '-'
                    else:
                        medium = '-'

                    if len(row) > 6:
                        place = row[6]
                        if place == '':
                            place = '-'
                    else:
                        place = '-'

                    # (imdbID, EAN, title, titleorig, titlelocal, medium, nr, source) = \
                    #     row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]

                    if imdbID != '' and imdbID != '0000000':
                        dbc.insertMovieData(
                        inputMovieId=imdbID,
                        inputTitle=titlelocal,
                        place=place,
                        medium=medium
                        )
                    else: # rows without imdbId
                        dbc.addManMovieWithoutIdToDb(
                            inputTitle=titlelocal,
                            place=place,
                            medium=medium
                            )