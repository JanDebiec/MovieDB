from flask import Blueprint, render_template, flash, redirect, url_for

from app import db
from app.mod_db.models import Movie, Role, People, Director

mod_db = Blueprint('database', __name__, url_prefix='/database')

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
    newMovie = Movie(imdbId=inputMovieId, titleLocal=inputTitle,
                     medium = medium,source = source)
    db.session.add(newMovie)
    db.session.commit()


def updateMovieInDb(movieId, inputTitle, medium, source):
    found = Movie.query.filter_by(imdbId= movieId)
    found.titleLocal = inputTitle
    found.medium = medium
    found.source = source
    db.session.commit()
