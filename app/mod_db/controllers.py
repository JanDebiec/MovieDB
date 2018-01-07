from flask import Blueprint, render_template, flash, redirect, url_for

from app import db
from app.mod_db.models import Movie, Role, People, Director
from app.mod_db.forms import SearchDbForm, SingleResultForm

import app.mod_imdb.controllers as tsv

mod_db = Blueprint('database', __name__, url_prefix='/mod_db')

@mod_db.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchDbForm()
    foundMessage = 'search'
    # init content of form

    if form.validate_on_submit():
        # try to search, result => found
        foundList = searchInDb(form)
        resultCount = len(foundList)
        if resultCount > 0:
            if resultCount == 1:
                return redirect('result')
            else:
                return redirect('movielist')
        else:
            foundMessage = 'No movie found, search once more'
    # show form with proper message
    return render_template('mod_db/search.html',
                            title='Search Movie',
                            form=form,
                            message=foundMessage)

@mod_db.route('/singleresult', methods=['GET', 'POST'])
def singleresult():
    form = SingleResultForm()
    return render_template('mod_db/singleresult.html',
                           title='Movie Result',
                           form=form)

@mod_db.route('/pageresults', methods=['GET', 'POST'])
def pageresults():
    pass

def searchInDb(flaskForm):
    ''' extract items from form,
    search for all movies, that fulfils the criteria
    return the list of all results'''
    result = []
    return result

def insertMovieData(inputMovieId, inputTitle='', medium='', source=''):
    '''insert data from input into db
    Data from Input (manual or csv) has structure:
    imdbId 7 char obligatory
    title (local title) optional
    medium optional
    source otpional
    If imdbId not found in db, then add item to db
    else add(modify) items already present
    '''
    dbMovie = searchDb(inputMovieId)
    if dbMovie == None:
        addManMovieToDb(inputMovieId, inputTitle, medium, source)
    else:
        updateMovieInDb(inputMovieId, inputTitle, medium, source)


def searchDb(movieId):
    ''' search local db for movie,
    return set of data if found, or None if not found'''
    found = Movie.query.filter_by(imdbId= movieId).first()
    return found


def addManMovieToDb(inputMovieId, inputTitle='', medium='', source=''):
    '''
    first search local imdb data for item, extract infos about
    movie, director, rating
    then insert new data set to db
    '''

    # get data from imdb tsv
    imdbData = tsv.getMovieData(inputMovieId)
    titleImdb=''
    titleOrig=''
    year = ''
    director = ''
    # prepare data for
    if imdbData != None:
        titleImdb = imdbData[0]
        if len(imdbData) > 1:
            titleOrig = imdbData[1]
            if len(imdbData) > 2:
                year = imdbData[2]
                if len(imdbData) > 4: # director
                    director = imdbData[4]

    newMovie = Movie(imdbId=inputMovieId,
                     titleImdb=titleImdb,
                     titleOrig=titleOrig,
                     titleLocal=inputTitle,
                     medium = medium,
                     year = year,
                     directors = director,
                     source = source)

    db.session.add(newMovie)
    db.session.commit()


def updateMovieInDb(movieId, inputTitle, medium, source):
    found = Movie.query.filter_by(imdbId= movieId).first()
    found.titleLocal = inputTitle
    found.medium = medium
    found.source = source
    db.session.commit()

# def updateMovieWithTsv(movieId):
#     found = Movie.query.filter_by(imdbId= movieId).first()
