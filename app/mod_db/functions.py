import json
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template

from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic, Rating
# from app.mod_db.forms import EditCriticForm, CriticsListForm, SearchDbForm, SingleResultForm, EditMovieForm, DeleteMovieForm, ExploreForm, PageResultsForm

import app.mod_imdb.controllers as tsv

class MovieToDisplay:

    def __init__(self, imdbId='',  titleImdb='', titleOrig='', titleLocal='',
                 director='', year='', medium='', linelength=0, source='', place='', EAN='',
                 ownerrating='',
                 amgrating='',
                 imdbrating=''):
        self.imdbId = imdbId
        self.titleImdb = titleImdb
        self.titleOrig = titleOrig
        self.titleLocal = titleLocal
        self.year = year
        self.medium = medium
        self.source = source
        self.place = place
        self.EAN = EAN
        self.director = director
        self.linelength = linelength
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
        imdbId=movie.imdbId,
        titleImdb=movie.titleImdb,
        titleOrig=movie.titleOrig,
        titleLocal=movie.titleLocal,
        director=movie.director.name,
        year=movie.year,
        medium=movie.medium,
        linelength=movie.linelength,
        source=movie.source,
        place=movie.place,
        EAN=movie.EAN,
        ownerrating = ratingDict['JD'],
        amgrating = ratingDict['AMG'],
        imdbrating = ratingDict['Imdb']
        )
    return movieToDisplay

def findOwnerRatings(movieList):
    ratings = []
    return ratings


def updateOwnerRatingInDb(foundList, inputRating):
    pass


def updateMediumInDb(foundList, inputMedium):
    pass


def updateImdbidInDb(foundList, inputImdbid):

    for i in range(len(foundList)):
    # for movie in foundList:
        movie = foundList[i]
        dbId = movie.imdbId
        if dbId == '' or dbId == '0000000':
            inputId = inputImdbid[i]
            if inputId != '' and inputId != '0000000':
                movie.imdbId = inputId
                updateMovieWithoutIDWithImdb(movie, inputId,)


def searchInDb(searchitems):
    ''' extract items from searchitems,
    search for all movies, that fulfils the criteria
    return the list of all results'''
    queryStarted = False
    itemimdbid = searchitems['imdbid']
    if itemimdbid != '':
        queryresult = Movie.query.filter_by(imdbId=itemimdbid)
        queryStarted = True

    itemmedium = searchitems['medium']
    if itemmedium != '':
        looking_for = '%{0}%'.format(itemmedium)
        if queryStarted == False:
            # for testing:
            queryresult = Movie.query.filter(Movie.medium.like(looking_for))
            # queryresult = Movie.query.filter_by(medium=itemmedium)
            queryStarted = True
        else:
            queryresult = queryresult.filter(Movie.medium.like(looking_for))
            # queryresult = queryresult.filter_by(medium=itemmedium)

    itemtext = searchitems['text']
    if itemtext != '':
        if queryStarted == False:
            queryresult = Movie.query.filter_by(titleLocal=itemtext)
            queryStarted = True
        else:
            queryresult = queryresult.filter_by(titleLocal=itemtext)

    itemyear = searchitems['year']
    if itemyear != '':
        if queryStarted == False:
            queryresult = Movie.query.filter_by(year=itemyear)
            queryStarted = True
        else:
            queryresult = queryresult.filter_by(year=itemyear)

    itemdirector = searchitems['director']
    if itemdirector != '':
        looking_for = '%{0}%'.format(itemdirector)
        dir = Director.query.filter(Director.name.like(looking_for)).first()
        dirid = dir.id
        if queryStarted == False:
            queryresult = Movie.query.filter_by(directors=dirid)
            queryStarted = True
        else:
            queryresult = queryresult.filter_by(directors=dirid)
    found = queryresult.all()
    return found


def insertMovieData(inputMovieId, inputTitle='', medium='', source='', place=''):
    '''insert data from input into db
    Data from Input (manual or csv) has structure:
    imdbId 7 char obligatory
    title (local title) optional
    medium optional
    source otpional
    If imdbId not found in db, then add item to db
    else add(modify) items already present
    '''
    dbMovie = None
    try:
        dbMovie = searchDb(inputMovieId)
    except:
        pass
    if dbMovie == None:
        addManMovieToDb(inputMovieId, inputTitle, medium, source, place)
    else:
        updateMovieManual(inputMovieId, inputTitle, medium, source, place)


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
        pass
    return found


def addManMovieToDb(inputMovieId, inputTitle='', medium='', source='', place=''):
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
            pass
    db.session.add(newMovie)
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


def updateMovieManual(movieId, inputTitle, medium, source, place):

    found = Movie.query.filter_by(imdbId= movieId).first()
    found.titleLocal = inputTitle
    found.medium = medium
    found.source = source
    found.place = place
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

def updateMovie(movieid, form):
    '''
    movie without imdbId can get imdbId,
    rest can get new medium (bought dvd) or user rating
    :param movieid: db id
    :param form: UpdateMovieForm to extract input data
    '''
    obj = Movie.query.filter_by(id=movieid).first()
    imdbId = form.imdbid.data

    ownRatingNew = form.ownrating.data
    jd = Critic.query.filter_by(name='JD').first()
    ownRatingOldObj = getRatingForMovie(obj, jd)
    if ownRatingOldObj != None:
        ownRatingOld = ownRatingOldObj.value
    else:
        ownRatingOld = None
    if(ownRatingNew != ownRatingOld) and (ownRatingNew != ''):
        if(ownRatingOldObj == None):
            newRating = Rating(movie_id=obj.id, critic_id=jd.id, value=ownRatingNew)
            # rat = Rating(movie_id=newMovie.id, critic_id=critic.id, value=ratData)
            db.session.add(newRating)
        else:
            ownRatingOldObj.value = ownRatingNew

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
        pass
    return ownRating


