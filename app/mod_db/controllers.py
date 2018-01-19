import json
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template

from app import db
from app.mod_db.models import Movie, Role, People, Director
from app.mod_db.forms import SearchDbForm, SingleResultForm, DeleteMovieForm, ExploreForm, PageResultsForm

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

        searchitems = json.dumps(searchdir)
        return redirect(url_for('database.pageresults', searchitems=searchitems))

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

@mod_db.route('/delete/<movieid>', methods=['GET', 'POST'])
def delete(movieid):
    form = DeleteMovieForm()
    movie = Movie.query.filter_by(id=movieid).first()

    # display the single result
    movietxt = movie
    form.imdbid.data = movie.imdbId
    form.imdbname.data = movie.titleImdb
    form.year.data = movie.year
    form.medium.data = movie.medium
    form.director.data = movie.director.name

    return render_template('mod_db/delete.html',
                           title='Movie Result',
                           moviemsg=movietxt,
                           form=form)

@mod_db.route('/pageresults/<searchitems>', methods=['GET', 'POST'])
def pageresults(searchitems):
    form = PageResultsForm()
    # we need the results of search onSubmit too,
    # to update the medium and ratings
    searchdir = json.loads(searchitems)
    foundList = searchInDb(searchdir)
    ownerRatings = []
    resultCount = len(foundList)
    if resultCount != 0:
        ownerRatings = findOwnerRatings(foundList)
        # TODO add ratings to foundList
    if form.validate_on_submit():
        if request.method == 'POST':
            userinputs = request.form
            newdict = userinputs.to_dict()
            amount = len(newdict)
            # we do not know the amount of ratings or medium
            # we know only global size of input
            inputImdbId = []
            for i in range(resultCount):
                try:
                    pointerString = 'imdbid[{}]'.format(i)
                    id = newdict[pointerString]
                    inputImdbId.append(id)
                except: # no more ratings
                    break
            # extracting user ratings input
            inputRating = []
            for i in range(resultCount):
                try:
                    pointerString = 'rating[{}]'.format(i)
                    rat = newdict[pointerString]
                    inputRating.append(rat)
                except: # no more ratings
                    break
            # extracting user medium input
            inputMedium = []
            for i in range(resultCount):
                try:
                    pointerString = 'medium[{}]'.format(i)
                    med = newdict[pointerString]
                    inputMedium.append(med)
                except: # no more medium input
                    break

            # TODO take inputs and insert in DB
            updateOwnerRatingInDb(foundList, inputRating)
            updateMediumInDb(foundList, inputMedium)
            updateImdbidInDb(foundList, inputImdbId)

        foundMessage = "search once more"
        return redirect(url_for('database.search', message=foundMessage))
    # searchdir = json.loads(searchitems)
    # foundList = searchInDb(searchdir)
    # ownerRatings = []
    # resultCount = len(foundList)
    if resultCount == 0:
        foundMessage = 'No movie found, search once more'
        return redirect(url_for('database.search', message=foundMessage))
    return render_template('mod_db/pageresults.html',
                           title='Movie Result',
                           form=form,
                           moviescount=resultCount,
                           movies=foundList
                           )


@mod_db.route('/explore', methods=['GET', 'POST'])
def explore():
    form = ExploreForm()
    found = Movie.query.filter_by(year='2014').all()
    movies = found
    # movies = found[0:4]
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)

    return render_template('mod_db/explore.html',
                           title='Movie Result',
                           form=form,
                           movies=movies)

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


def addManMovieWithoutIdToDb(inputTitle='', medium='-', source=''):
    '''
    '''
    newMovie = Movie(
        imdbId='0000000',
                     titleLocal=inputTitle,
                     medium = medium,
                     source = source)
    db.session.add(newMovie)
    db.session.commit()


def updateMovieWithoutIDWithImdb(movie, imdbid):

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
        else:
            director = dirInDb
        movie.director = director

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

def deleteObj():
    obj = Movie.query.filter_by(id=123).first()
    if len(obj) == 1:
        db.session.delete(obj[0])
        db.session.commit()