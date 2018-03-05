import json
import sys
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template
from flask import current_app
from sqlalchemy import or_

from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic, Rating
# from app.mod_db.forms import EditCriticForm, CriticsListForm, SearchDbForm, SingleResultForm, EditMovieForm, DeleteMovieForm, ExploreForm, PageResultsForm

import app.mod_imdb.controllers as tsv
from  helper import clock # decorator clock

class MovieToDisplay:

    def __init__(self,
                 movie,
                 ownerrating='',
                 amgrating='',
                 imdbrating=''):
        self.id = movie.id
        self.imdbId = movie.imdbId
        self.titleImdb = movie.titleImdb
        self.titleOrig = movie.titleOrig
        self.titleLocal = movie.titleLocal
        self.year = movie.year
        self.medium = movie.medium
        self.source = movie.source
        self.place = movie.place
        self.EAN = movie.EAN
        try:
            self.director = movie.director.name
        except:
            self.director = ''
        self.linelength = movie.linelength
        self.ownerrating = ownerrating
        self.amgrating = amgrating
        self.imdbrating = imdbrating

def findAllRatingsForMovie(movie):

    ratingDict = {}
    criticsList = Critic.query.all()

    for critic in criticsList:
        rating = getRatingForMovie(movie, critic)
        if rating != None:
            ratingDict[critic.name] = rating.value
        else:
            ratingDict[critic.name] = ''
    return  ratingDict


def convertMovieToDIsplay(movie):

    ratingDict = findAllRatingsForMovie(movie)

    movieToDisplay = MovieToDisplay(
        movie,
        ownerrating = ratingDict['JD'],
        amgrating = ratingDict['AMG'],
        imdbrating = ratingDict['Imdb']
        )
    return movieToDisplay


def updateImdbidInDb(foundList, inputImdbid):

    for inputId, movie in zip(inputImdbid, foundList):
        dbId = movie.imdbId
        if dbId == '' or dbId == '0000000':
            if inputId != '' and inputId != '0000000':
                movie.imdbId = inputId
                updateMovieWithoutIDWithImdb(movie, inputId,)


@clock
def searchInDb(searchitems):
    ''' extract items from searchitems,
    search for all movies, that fulfils the criteria
    return the list of all results'''
    queryStarted = False
    found = None
    itemimdbid = searchitems['imdbid']
    if itemimdbid != '':
        queryresult = Movie.query.filter_by(imdbId=itemimdbid)
        queryStarted = True

    # only equal reults, DVD and excluded DVDR
    itemmedium = searchitems['medium']
    if itemmedium != '':
        looking_for = '%{0}%'.format(itemmedium)
        if queryStarted == False:
            # for testing:
            # queryresult = Movie.query.filter(Movie.medium.like(looking_for))
            queryresult = Movie.query.filter_by(medium=itemmedium).order_by(Movie.year.desc())
            queryStarted = True
        else:
            # queryresult = queryresult.filter(Movie.medium.like(looking_for))
            queryresult = queryresult.filter_by(medium=itemmedium).order_by(Movie.year.desc())


    itemtext = searchitems['text']
    if itemtext != '':
        looking_for = '%{0}%'.format(itemtext)
        if queryStarted == False:
            # queryresult = Movie.query.filter_by(titleLocal=itemtext)
            queryresult = Movie.query.filter(Movie.titleLocal.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Movie.titleLocal.like(looking_for))

    itemyear = searchitems['year']
    if itemyear != '':
        if queryStarted == False:
            queryresult = Movie.query.filter_by(year=itemyear)
            queryStarted = True
        else:
            queryresult = queryresult.filter_by(year=itemyear)

    itemplace = searchitems['place']
    looking_for = '%{0}%'.format(itemplace)
    if itemplace != '':
        if queryStarted == False:
            # queryresult = Movie.query.filter_by(place=itemplace)
            queryresult = Movie.query.filter(Movie.place.like(looking_for))
            queryStarted = True
        else:
            queryresult = queryresult.filter(Movie.place.like(looking_for))

    itemdirector = searchitems['director']
    if itemdirector != '':
        looking_for = '%{0}%'.format(itemdirector)
        dirs = Director.query.filter(Director.name.like(looking_for)).all()
        if dirs != None:
            dirid = [dir.id for dir in dirs]
            if queryStarted == False:
                count = len(dirid)
                if count == 1:
                    queryresult = Movie.query.filter_by(directors=dirid[0]).order_by(Movie.year.desc())
                elif count == 2:
                    queryresult = Movie.query.filter(or_(Movie.directors == dirid[0], Movie.directors == dirid[1])).order_by(Movie.year.desc())
                queryStarted = True
            else:
                queryresult = queryresult.filter_by(directors=dirid).order_by(Movie.year.desc())

    if  queryStarted:
        found = queryresult.all()


    return found


def searchAmgInWholeDb():
    ''' extract items from searchitems,
    search for all movies, that fulfils the criteria
    return the list of all results'''
    found = []
    return found

def filterMoviesWithAmgRating(found, itemamg):
    listWithRating = []
    minimalRating = float(itemamg)
    for movie in found:
        actRating = movie.amgrating
        try:
            actfloat = float(actRating)
        except:
            actfloat = 0.0
        if actfloat >= minimalRating:
            listWithRating.append(movie)

    return listWithRating

def filterMoviesWithCriticRating(found, critic, rating):
    listWithRating = []
    minimalRating = float(rating)
    for movie in found:
        if critic == 'AMG':
            actRating = movie.amgrating
        elif critic == 'JD':
            actRating = movie.ownerrating
        elif critic == 'Imdb':
            actRating = movie.imdbrating

        try:
            actfloat = float(actRating)
        except:
            actfloat = 0.0
        if actfloat >= minimalRating:
            listWithRating.append(movie)

    return listWithRating

def insertMovieDataFromForm(singleMovieForm):
    dbMovie = None
    inputMovieId = singleMovieForm.imdbid.data
    if inputMovieId != '' and inputMovieId != '0000000':
        try:
            dbMovie = searchDb(inputMovieId)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    if dbMovie == None:
        localname = singleMovieForm.localname.data
        medium = singleMovieForm.medium.data
        place = singleMovieForm.place.data
        ownrating = singleMovieForm.ownrating.data
        amgrating = singleMovieForm.amgrating.data
        source = ''
        addManMovieToDb(inputMovieId, localname, medium, source, place, ownrating, amgrating)
    else:
        updateMovie(inputMovieId, singleMovieForm)
        # updateMovieManual(inputMovieId, inputTitle, medium, source, place, ownrating, amgrating)


def insertMovieData(inputMovieId,
                    inputTitle='', medium='',
                    source='', place='',
                    ownrating='',
                    amgrating=''):
    '''insert data from input into db,
    used in parsing csv files.
    Data from Input (csv) has structure:
    imdbId 7 char obligatory
    title (local title) optional
    medium optional
    source otpional
    If imdbId not found in db, then add item to db
    else add(modify) items already present
    '''
    dbMovie = None
    if inputMovieId != '' and inputMovieId != '0000000':
        try:
            dbMovie = searchDb(inputMovieId)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    if dbMovie == None:
        addManMovieToDb(inputMovieId, inputTitle, medium, source, place, ownrating, amgrating)
    else:
        updateMovieManual(inputMovieId, inputTitle, medium, source, place, ownrating, amgrating)


def searchDb(movieId):
    ''' search local db for movie,
    return set of data if found, or None if not found'''
    found = Movie.query.filter_by(imdbId= movieId).first()
    return found


def searchDirectorDb(peopleId):
    ''' search local db for movie,
    return set of data if found, or None if not found'''
    found = None
    try:
        found = Director.query.filter_by(peopleImdbId= peopleId).first()
    except:
        current_app.logger.error('director not found', exc_info=sys.exc_info())
        pass
    return found


def addManMovieToDb(inputMovieId,
                    inputTitle='', medium='',
                    source='', place='',
                    ownrating='',
                    amgrating=''):
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
    length = 0
    if imdbData != None:
        length = imdbData[0]
        titleImdb = imdbData[1]
        if len(imdbData) > 2:
            titleOrig = imdbData[2]
            if len(imdbData) > 3:
                year = imdbData[3]

    newMovie = Movie(imdbId=inputMovieId,
                     titleImdb=titleImdb,
                     titleOrig=titleOrig,
                     titleLocal=inputTitle,
                     medium = medium,
                     year = year,
                     linelength = length,
                     place = place,
                     source = source)
    db.session.add(newMovie)

    dirData = tsv.getMovieDirector(inputMovieId)
    if dirData != None:
        directorId = dirData
        dirInDb = searchDirectorDb(directorId)
        if dirInDb == None:
            dirName = tsv.getNameData(directorId)
            director = Director(peopleImdbId=directorId, name=dirName)
            db.session.add(director)
        else:
            director = dirInDb
        newMovie.director = director

    ratData = tsv.getMovieRating(inputMovieId)
    if ratData != None:
        try:
            critic = Critic.query.filter_by(name='Imdb').first()
            rat = Rating(movie_id=newMovie.id, critic_id=critic.id, value=ratData)
            db.session.add(rat)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
            pass

    if ownrating != '':
        try:
            critic = Critic.query.filter_by(name='JD').first()
            rat = Rating(movie_id=newMovie.id, critic_id=critic.id, value=ownrating)
            db.session.add(rat)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
            pass

    if amgrating != '':
        try:
            critic = Critic.query.filter_by(name='AMG').first()
            rat = Rating(movie_id=newMovie.id, critic_id=critic.id, value=amgrating)
            db.session.add(rat)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
            pass

    db.session.commit()


def addManMovieWithoutIdToDb(inputTitle='', medium='-', source='', place=''):
    '''
    '''
    newMovie = Movie(
        imdbId='0000000',
                     titleLocal=inputTitle,
                     medium = medium,
                     place=place,
                     source = source)
    db.session.add(newMovie)
    db.session.commit()


def updateMovieWithoutIDWithImdb(movie, imdbid, commit=True):

    # search imdb for movie
    # get data from imdb tsv
    imdbData = tsv.getMovieData(imdbid)
    titleImdb=''
    titleOrig=''
    year = ''
    director = ''
    # prepare data for
    length = 0
    if imdbData != None:
        length = imdbData[0]
        titleImdb = imdbData[1]
        if len(imdbData) > 2:
            titleOrig = imdbData[2]
            if len(imdbData) > 3:
                year = imdbData[3]

    movie.imdbId=imdbid
    movie.titleImdb=titleImdb
    movie.titleOrig=titleOrig
    movie.year = year
    movie.linelength = length
    dirData = tsv.getMovieDirector(imdbid)
    if dirData != None:
        directorId = dirData
        dirInDb = searchDirectorDb(directorId)
        if dirInDb == None:
            dirName = tsv.getNameData(directorId)
            director = Director(peopleImdbId=directorId, name=dirName)
            db.session.add(director)
        else:
            director = dirInDb
        movie.director = director

    if commit:
        db.session.commit()


def updateMovieManual(movieId, inputTitle, medium, source, place, ownrating, amgrating):

    found = Movie.query.filter_by(imdbId= movieId).first()
    found.titleLocal = inputTitle
    found.medium = medium
    found.source = source
    found.place = place

    try:
        critic = Critic.query.filter_by(name='JD').first()
        rat = Rating(movie_id=found.id, critic_id=critic.id, value=ownrating)
        db.session.add(rat)
        critic = Critic.query.filter_by(name='AMG').first()
        rat = Rating(movie_id=found.id, critic_id=critic.id, value=amgrating)
        db.session.add(rat)
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass


    db.session.commit()


def updateMovieWithTsv(movieId):

    found = Movie.query.filter_by(imdbId=movieId).first()

    tsvLengthNew = 0
    tsvLengthOld = found.linelength
    imdbData = tsv.getMovieData(movieId)
    if imdbData != None:
        tsvLengthNew = imdbData[0]

    if tsvLengthNew > tsvLengthOld:
        # titleImdb = ''
        # titleOrig = ''
        # year = ''
        # director = ''
        # # prepare data for
        # length = imdbData[0]
        titleImdb = imdbData[1]
        found.titleImdb = titleImdb
        if len(imdbData) > 2:
            titleOrig = imdbData[2]
            found.titleOrig = titleOrig
            if len(imdbData) > 3:
                year = imdbData[3]
                found.year = year

        db.session.commit()

def deleteMovie(movieid):
    obj = Movie.query.filter_by(id=movieid).first()
    print(obj)
    db.session.delete(obj)
    db.session.commit()

def upgradeMovie(movieid, form):
    '''
    there are some movies added to DB with known ImdbId, but not listed
    in actual tsv files. with the new version of tsv,
    movie can be upgraded, t.i. some new infirmations *director, rating)
    can be added to own DB
    :param movieid:
    :param form:
    :return:
    '''
    try:
        obj = Movie.query.filter_by(id=movieid).first()
        imdbId = form.imdbid.data
        updateMovieWithoutIDWithImdb(obj, imdbId)

    except:
        current_app.logger.error('upgrade not succeded', exc_info=sys.exc_info())

def updateMovie(movieid, form):
    '''
    movie without imdbId can get imdbId,
    rest can get new medium (bought dvd) or user rating
    :param movieid: db id
    :param form: UpdateMovieForm to extract input data
    '''
    obj = Movie.query.filter_by(id=movieid).first()
    imdbId = form.imdbid.data

    amgRatingNew = form.ratingAmg.data
    amg = Critic.query.filter_by(name='AMG').first()
    updateRating(obj, amg, amgRatingNew)

    ownRatingNew = form.ownrating.data
    jd = Critic.query.filter_by(name='JD').first()
    updateRating(obj, jd, ownRatingNew)

    oldTitle = obj.titleLocal
    newTitle = form.localname.data
    if newTitle != oldTitle:
        obj.titleLocal = newTitle

    oldMedium = obj.medium
    newMedium = form.medium.data
    if newMedium != oldMedium:
        obj.medium = newMedium

    newplace = form.place.data
    oldplace = obj.place
    if newplace != oldplace:
        obj.place = newplace

    oldImdb = obj.imdbId
    if oldImdb == '' or oldImdb == '0000000':
        if imdbId != '' and imdbId != '0000000':
            updateMovieWithoutIDWithImdb(obj, imdbId, commit=False)
    db.session.commit()

def updateRating(movie, critic, newRating):

    ratingOldObj = getRatingForMovie(movie, critic)
    if ratingOldObj != None:
        ownRatingOld = ratingOldObj.value
    else:
        ownRatingOld = None
    if(newRating != ownRatingOld) and (newRating != ''):
        if(ratingOldObj == None):
            newRating = Rating(movie_id=movie.id, critic_id=critic.id, value=newRating)
            db.session.add(newRating)
        else:
            ratingOldObj.value = newRating


def updateCritic(criticid, form):
    obj = Critic.query.filter_by(id=criticid).first()
    name = form.name.data
    url = form.url.data
    maxVal = form.maxval.data
    obj.name = name
    obj.url = url
    obj.maxVal = maxVal
    db.session.commit()



def getRatingForMovie(movieobj, criticobj):
    object = None
    try:
        ownRatings = Rating.query.filter_by(critic_id=criticobj.id)
        rating = ownRatings.filter_by(movie_id=movieobj.id).first()
        object = rating
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass
    return object

def getJdRatingForMovie(movieobj):
    ownRating = None
    try:
        jd = Critic.query.filter_by(name='JD').first()
        ownRatingObj = getRatingForMovie(movieobj, jd)
        if ownRatingObj != None:
            ownRating = ownRatingObj.value
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass
    return ownRating

def getAmgRatingForMovie(movieobj):
    amgRating = None
    try:
        amg = Critic.query.filter_by(name='AMG').first()
        amgRatingObj = getRatingForMovie(movieobj, amg)
        if amgRatingObj != None:
            amgRating = amgRatingObj.value
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass
    return amgRating


def updateOwnerRatingInDb(foundList, inputRating):
    owner = Critic.query.filter_by(name='JD').first()
    for rating, movie in zip(inputRating, foundList):
        updateRating(movie, owner, rating)

def updateAmgRatingInDb(foundList, inputRating):
    amg = Critic.query.filter_by(name='AMG').first()
    for rating, movie in zip(inputRating, foundList):
        updateRating(movie, amg, rating)

def updateMediumInDb(foundList, inputMedium):
    for movie, newMedium in zip(foundList, inputMedium):
        oldMedium = movie.medium
        if newMedium != oldMedium:
            movie.medium = newMedium

def updatePlaceInDb(foundList, inputPlace):
    for movie, newPlace in zip(foundList, inputPlace):
        oldPlace = movie.place
        if newPlace != oldPlace:
            movie.place = newPlace

# def insertManualInput(manInputForm):
#     ''' extract data from InputForm,
#     validate and insert/update in db,
#     check if movie already exist, if so only update.
#     using form as parameter
#     '''
#     imdbid = manInputForm.imdbid.data
#     localname = manInputForm.localname.data
#     medium = manInputForm.medium.data
#     place = manInputForm.place.data
#     ownrating = manInputForm.ownrating.data
#     amgrating = manInputForm.amgrating.data
#
#     # flash('Added Movie: Id={}, localName={}, medium={}'.format(
#     #     imdbid, localname, medium
#     # ))
#     insertMovieDataFromForm(inputMovieId=imdbid,
#                         inputTitle=localname,
#                         medium=medium,
#                         place=place,
#                         ownrating=ownrating,
#                         amgrating=amgrating)

