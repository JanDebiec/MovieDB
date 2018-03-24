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
import app.mod_critics.metacritics as mc
from  helper import clock # decorator clock

class MovieToDisplay:

    def __init__(self,
                 movie,
                 ownerrating='',
                 amgrating='',
                 mcrating='',
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
        self.mcrating = mcrating

def findReferenceRatingsForMovie(movie):
    '''
    only ratings from JD, AMG, MC will be shown in the display
    :param movie:
    :return:
    '''
    critic_reference_list = ['JD', 'AMG', 'MC']
    ratingDict = {}
    criticsList = []
    for item in critic_reference_list:
        critic = Critic.query.filter_by(name=item).first()
        if critic != None:
            criticsList.append(critic)

    for critic in criticsList:
        rating = getRatingObjForMovie(movie, critic)
        if rating != None:
            ratingDict[critic.name] = rating.value
        else:
            ratingDict[critic.name] = ''
    return  ratingDict


def convertMovieToDIsplay(movie):

    ratingDict = findReferenceRatingsForMovie(movie)

    movieToDisplay = MovieToDisplay(
        movie,
        ownerrating = ratingDict['JD'],
        mcrating = ratingDict['MC'],
        amgrating = ratingDict['AMG']
        )
    return movieToDisplay

@clock
def convert_list_to_display(foundMovieList):
    list_ = []
    for movie in foundMovieList:
        movieToDisplay = convertMovieToDIsplay(movie)
        list_.append(movieToDisplay)
    return list_


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
        amgrating = singleMovieForm.ratingAmg.data
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

# def updateMovieMetacrit(movieid, form):
#     movie = Movie.query.filter_by(id=movieid).first()
#     mc.get_update_movie_ratings(movie)
#
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

    ratingOldObj = getRatingObjForMovie(movie, critic)
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



def getRatingObjForMovie(movieobj, critic_obj):
    object = None
    # critic = Critic.query.filter_by(name=critic_name).first()
    try:
        ownRatings = Rating.query.filter_by(critic_id=critic_obj.id)
        rating = ownRatings.filter_by(movie_id=movieobj.id).first()
        object = rating
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass
    return object

def getRatingValueForMovie(movieobj, critic_name):
    rating = None
    try:
        critic = Critic.query.filter_by(name=critic_name).first()
        ratingObj = getRatingObjForMovie(movieobj, critic)
        if ratingObj != None:
            rating = ratingObj.value
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass
    return rating


def getJdRatingForMovie(movieobj):
    ownRating = None
    try:
        jd = Critic.query.filter_by(name='JD').first()
        ownRatingObj = getRatingObjForMovie(movieobj, jd)
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
        amgRatingObj = getRatingObjForMovie(movieobj, amg)
        if amgRatingObj != None:
            amgRating = amgRatingObj.value
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass
    return amgRating

def getMcRatingForMovie(movieobj):
    mcRating = None
    try:
        mc = Critic.query.filter_by(name='MC').first()
        mcRatingObj = getRatingObjForMovie(movieobj, mc)
        if mcRatingObj != None:
            mcRating = mcRatingObj.value
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        pass
    return mcRating


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

def add_critic(critic_object):
    '''
    check if critic already exists,
    if not insert
    :param critic_object:
    :return: critic_id
    '''
    try:
        obj = Critic.query.filter_by(name=critic_object.name).first()
        if obj == None:
            db.session.add(critic_object)
            db.session.commit()
        real_obj = Critic.query.filter_by(name=critic_object.name).first()
        id = real_obj.id
        return id
    except:
        current_app.logger.error('critic not added', exc_info=sys.exc_info())
        return 0

def add_rating(rating_obj):
    '''
    check if rating already exist,
    if yes, modify
    if not, insert
    :param rating_obj:
    :return:
    '''
    try:
        crit_query = Rating.query.filter_by(critic_id=rating_obj.critic_id)
        old_rating = crit_query.filter_by(movie_id=rating_obj.movie_id).first()
        if old_rating != None:
            # update
            old_rating.value = rating_obj.value
        else:
            db.session.add(rating_obj)
        db.session.commit()
    except:
        current_app.logger.error('rating not added', exc_info=sys.exc_info())

# @clock
def insert_rating_for_movie_from_html(movie_id, movie_html):
    mc_rating, count, list_ = mc.get_rating_list_for_movie(movie_id, movie_html)
    if mc_rating > 0:
        add_mc_rating_for_movie(mc_rating, movie_id)
    if count > 0:
        # add_mc_rating_for_movie(mc_rating, movie_id)

        for item in list_:
            name = '{}'.format(item.author) # only author, without newspaper
            name_mc = mc.convert_name_to_mc(name)
            url = 'http://www.metacritic.com/critic/{}?filter=movies'.format(name_mc)
            maxVal = 100.0
            crit_obj = Critic(name=name, url=url, maxVal=maxVal)
            crit_id = add_critic(crit_obj)
            rat = Rating(movie_id, critic_id=crit_id, value=item.rating)
            add_rating(rat)


def add_mc_rating_for_movie(mc_rating, movie_id):
    mc_crit_obj = Critic.query.filter_by(name='MC').first()
    if mc_crit_obj == None:
        mc_critic = Critic(name='MC', maxVal=100)
        crit_id = add_critic(mc_critic)
    else:
        crit_id = mc_crit_obj.id
    rat = Rating(movie_id, critic_id=crit_id, value=mc_rating)
    add_rating(rat)


def get_update_movie_ratings(movie_obj):
    movie_html = mc.get_movie_html(movie_obj)
    movie_id = movie_obj.id
    insert_rating_for_movie_from_html(movie_id, movie_html)

def updateMovieMetacrit(movieid, form):
    movie = Movie.query.filter_by(id=movieid).first()
    get_update_movie_ratings(movie)

@clock
def create_list_for_mc_download():
    critic_jd = Critic.query.filter_by(name='JD').first()
    critic_mc = Critic.query.filter_by(name='MC').first()
    JD_list = Rating.query.filter_by(critic_id=critic_jd.id).all()
    movie_dict = {}
    for rating in JD_list:
        movie = Movie.query.filter_by(id=rating.movie_id).first()
        query = Rating.query.filter_by(movie_id=movie.id)
        mc_ratings = query.filter_by(critic_id=critic_mc.id).all()
        # check if mc content already saved in DB
        # if not
        #     load mc data and save in DB
        if len(mc_ratings) == 0:
            movie_dict[rating.movie_id] = movie

    listWithRatings = list(movie_dict.values())
    return listWithRatings
