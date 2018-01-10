import json
from flask import Blueprint, render_template, flash, redirect, url_for

from app import db
from app.mod_db.models import Movie, Role, People, Director
from app.mod_db.forms import SearchDbForm, SingleResultForm, ExploreForm, PageResultsForm

import app.mod_imdb.controllers as tsv


mod_db = Blueprint('database', __name__, url_prefix='/mod_db')


@mod_db.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchDbForm()
    foundMessage = 'search'
    # init content of form
    searchdir = {}
    if form.validate_on_submit():
        searchdir['imdbid'] = form.imdbid.data
        searchdir['text'] = form.text.data
        searchdir['year'] = form.year.data
        searchdir['medium'] = form.medium.data
        searchdir['director'] = form.director.data

        # try to search, result => found
        # depending on resultsCout, the proper function will be called
        # and once more saerched
        # in such a way, we have the class with all members to display
        # in proper web page

        foundList = searchInDb(searchdir)
        resultCount = len(foundList)

        # for the single result, it's enought to transfer imdbid'
        # for multiple found, the searchdir should be transffered

        # if movies should be transferred, then it will be
        # transferred the representation (_repr) of the class
        # one option, first to search, check the results count,
        # then transfer to proper site the search filter
        # and in proper site search once more

        # for testing:
        # return redirect(url_for('database.pageresults', searchdir=searchdir))
        if resultCount > 0:
            foundMessage = 'search'
            if resultCount == 1:
                foundMovie = foundList[0]
                searchdir['imdbid'] = foundMovie.imdbId
                searchitems = json.dumps(searchdir)
                return redirect(url_for('database.singleresult', searchitems=searchitems))
            else:
                searchitems = json.dump(searchdir)
                return redirect(url_for('database.pageresults', searchitems=searchitems))
                # return redirect('singleresult', movie = 'Found Movie')
                # return redirect('pageresults', movies = foundList)
        else:
            foundMessage = 'No movie found, search once more'
    # show form with proper message
    return render_template('mod_db/search.html',
                            title='Search Movie',
                            form=form,
                            message=foundMessage)


@mod_db.route('/singleresult/<searchitems>', methods=['GET', 'POST'])
def singleresult(searchitems):
    form = SingleResultForm()
    searchdir = json.loads(searchitems)
    # build search command from searchitems
    idToSearch = searchdir['imdbid']

    # search once more
    movie = searchDb(idToSearch)

    # display the single result
    movietxt = movie
    form.imdbid.data = movie.imdbId
    form.imdbname.data = movie.titleImdb
    form.year.data = movie.year
    form.medium.data = movie.medium
    form.director.data = movie.director.name

    return render_template('mod_db/singleresult.html',
                           title='Movie Result',
                           moviemsg=movietxt,
                           form=form)



@mod_db.route('/pageresults/<searchitems>', methods=['GET', 'POST'])
def pageresults(searchitems):
    form = PageResultsForm()
    return render_template('mod_db/pageresults.html',
                           title='Movie Result',
                           form=form,
                           movies=searchitems)


@mod_db.route('/explore', methods=['GET', 'POST'])
def explore():
    form = ExploreForm()
    found = Movie.query.filter_by(year='2016').all()
    movies = found[0:4]
    return render_template('mod_db/explore.html',
                           title='Movie Result',
                           form=form,
                           movies=movies)



def searchInDb(searchitems):
    ''' extract items from searchitems,
    search for all movies, that fulfils the criteria
    return the list of all results'''
    queryStarted = False
    itemimdbid = searchitems['imdbid']
    if itemimdbid != '':
        queryresult = Movie.query.filter_by(imdbid=itemimdbid)
        queryStarted = True
    itemmedium = searchitems['medium']
    if itemmedium != '':
        if queryStarted == False:
            queryresult = Movie.query.filter_by(medium=itemmedium)
            queryStarted = True
        else:
            queryresult = queryresult.filter_by(medium=itemmedium)
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
    # wull be used later
    # itemdirector = searchitems['director']
    found = queryresult.all()
    return found


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
        updateMovieManual(inputMovieId, inputTitle, medium, source)


def searchDb(movieId):
    ''' search local db for movie,
    return set of data if found, or None if not found'''
    found = Movie.query.filter_by(imdbId= movieId).first()
    return found


def searchDirectorDb(peopleId):
    ''' search local db for movie,
    return set of data if found, or None if not found'''
    found = Director.query.filter_by(peopleImdbId= peopleId).first()
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
                     source = source)
    dirData = tsv.getMovieDirector(inputMovieId)
    if dirData != None:
        directorId = dirData
        dirInDb = searchDirectorDb(directorId)
        if dirInDb == None:
            dirName = tsv.getNameData(directorId)
            director = Director(peopleImdbId=directorId, name=dirName)
        else:
            director = dirInDb
        newMovie.director = director

    db.session.add(newMovie)
    db.session.commit()


def updateMovieManual(movieId, inputTitle, medium, source):

    found = Movie.query.filter_by(imdbId= movieId).first()
    found.titleLocal = inputTitle
    found.medium = medium
    found.source = source
    db.session.commit()

def updateMovieWithTsv(movieId):

    found = Movie.query.filter_by(imdbId=movieId).first()

    tsvLengthNew = 0
    tsvLengthOld = found.linelength
    imdbData = tsv.getMovieData(movieId)
    if imdbData != None:
        tsvLengthNew = imdbData[0]

    if tsvLengthNew > tsvLengthOld:
        titleImdb = ''
        titleOrig = ''
        year = ''
        director = ''
        # prepare data for
        length = imdbData[0]
        titleImdb = imdbData[1]
        found.titleImdb = titleImdb
        if len(imdbData) > 2:
            titleOrig = imdbData[2]
            found.titleOrig = titleOrig
            if len(imdbData) > 3:
                year = imdbData[3]
                found.year = year

        db.session.commit()

