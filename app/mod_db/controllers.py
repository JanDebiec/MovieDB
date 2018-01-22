import json
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template

from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic, Rating
from app.mod_db.forms import EditCriticForm, CriticsListForm, SearchDbForm, SingleResultForm, EditMovieForm, DeleteMovieForm, ExploreForm, PageResultsForm

import app.mod_imdb.controllers as tsv

from app.mod_db.functions import *


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
    foundMessage = 'search'
    if form.validate_on_submit():
        deleteMovie(movieid)
        return redirect(url_for('database.search', message=foundMessage))

    # display the single result
    movie = Movie.query.filter_by(id=movieid).first()
    movietxt = movie
    try:
        form.imdbid.data = movie.imdbId
        form.imdbname.data = movie.titleImdb
        form.year.data = movie.year
        form.medium.data = movie.medium
        form.localname.data = movie.titleLocal
        form.director.data = movie.director.name
    except:
        pass
    return render_template('mod_db/delete.html',
                           title='Movie to delete',
                           moviemsg=movietxt,
                           form=form)


@mod_db.route('/edit/<movieid>', methods=['GET', 'POST'])
def edit(movieid):
    form = EditMovieForm()
    foundMessage = 'search'
    if form.validate_on_submit():
        updateMovie(movieid, form)
        return redirect(url_for('database.search', message=foundMessage))

    # display the single result
    movie = Movie.query.filter_by(id=movieid).first()
    movietxt = movie
    form.imdbid.data = movie.imdbId
    form.imdbname.data = movie.titleImdb
    form.year.data = movie.year
    form.medium.data = movie.medium
    form.place.data = movie.place
    form.localname.data = movie.titleLocal
    try:
        form.director.data = movie.director.name
    except:
        pass
    try:
        form.ownrating.data = getJdRatingForMovie(movie)
    except:
        pass
    return render_template('mod_db/edit.html',
                           title='Movie to edit',
                           moviemsg=movietxt,
                           form=form)

@mod_db.route('/pageresults/<searchitems>', methods=['GET', 'POST'])
def pageresults(searchitems):
    form = PageResultsForm()
    # we need the results of search onSubmit too,
    # to update the medium and ratings
    searchdir = json.loads(searchitems)
    foundMovieList = searchInDb(searchdir)

    #TODO convert every Movie into MovieToDiplay
    listMovieToDisplay = []
    for movie in foundMovieList:
        movieToDisplay = convertMovieToDIsplay(movie)
        listMovieToDisplay.append(movieToDisplay)
    # listMovieToDisplay = foundMovieList

    foundList = listMovieToDisplay
    resultCount = len(foundList)
    # if resultCount != 0:
    #     ownerRatings = findOwnerRatings(foundList)
    #     # TODO add ratings to foundList
    if form.validate_on_submit():
        if request.method == 'POST':
            userinputs = request.form
            newdict = userinputs.to_dict()
            amount = len(newdict)
            # we do not know the amount of ratings or medium
            # we know only global size of input

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

        foundMessage = "search once more"
        return redirect(url_for('database.search', message=foundMessage))

    if resultCount == 0:
        foundMessage = 'No movie found, search once more'
        return redirect(url_for('database.search', message=foundMessage))
    return render_template('mod_db/pageresults.html',
                           title='Movie Result',
                           form=form,
                           moviescount=resultCount,
                           # ownerRatings = ownerRatings,
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

@mod_db.route('/critics', methods=['GET', 'POST'])
def critics():
    form = CriticsListForm()
    found = Critic.query.all()
    critics = found
    # movies = found[0:4]
    # if request.method == 'POST':
    #     result = request.form
    #     return render_template("result.html", result=result)

    return render_template('mod_db/critics.html',
                           title='Critics list',
                           form=form,
                           critics=critics
                           )


@mod_db.route('/addcritic', methods=['GET', 'POST'])
def addcritic():
    pass


@mod_db.route('/deletecritic/<criticid>', methods=['GET', 'POST'])
def deletecritic(criticid):
    pass

    # form = DeleteMovieForm()
    # foundMessage = 'search'
    # if form.validate_on_submit():
    #     deleteMovie(movieid)
    #     return redirect(url_for('database.search', message=foundMessage))
    #
    # # display the single result
    # movie = Movie.query.filter_by(id=movieid).first()
    # movietxt = movie
    # try:
    #     form.imdbid.data = movie.imdbId
    #     form.imdbname.data = movie.titleImdb
    #     form.year.data = movie.year
    #     form.medium.data = movie.medium
    #     form.localname.data = movie.titleLocal
    #     form.director.data = movie.director.name
    # except:
    #     pass
    # return render_template('mod_db/deletecritic.html',
    #                        title='Movie to delete',
    #                        moviemsg=movietxt,
    #                        form=form)


@mod_db.route('/editcritic/<criticid>', methods=['GET', 'POST'])
def editcritic(criticid):
    form = EditCriticForm()
    if form.validate_on_submit():
        updateCritic(criticid, form)
        return redirect(url_for('database.critics'))

    # display the single result
    critic= Critic.query.filter_by(id=criticid).first()
    form.name.data = critic.name
    form.url.data = critic.url
    form.maxval.data = critic.maxVal
    return render_template('mod_db/editcritic.html',
                           title='Critic to edit',
                           form=form)




# def findOwnerRatings(movieList):
#     ratings = []
#     return ratings
#
#
# def updateOwnerRatingInDb(foundList, inputRating):
#     pass
#
#
# def updateMediumInDb(foundList, inputMedium):
#     pass
#
#
# def updateImdbidInDb(foundList, inputImdbid):
#
#     for i in range(len(foundList)):
#     # for movie in foundList:
#         movie = foundList[i]
#         dbId = movie.imdbId
#         if dbId == '' or dbId == '0000000':
#             inputId = inputImdbid[i]
#             if inputId != '' and inputId != '0000000':
#                 movie.imdbId = inputId
#                 updateMovieWithoutIDWithImdb(movie, inputId,)
#
#
# def searchInDb(searchitems):
#     ''' extract items from searchitems,
#     search for all movies, that fulfils the criteria
#     return the list of all results'''
#     queryStarted = False
#     itemimdbid = searchitems['imdbid']
#     if itemimdbid != '':
#         queryresult = Movie.query.filter_by(imdbId=itemimdbid)
#         queryStarted = True
#
#     itemmedium = searchitems['medium']
#     if itemmedium != '':
#         looking_for = '%{0}%'.format(itemmedium)
#         if queryStarted == False:
#             # for testing:
#             queryresult = Movie.query.filter(Movie.medium.like(looking_for))
#             # queryresult = Movie.query.filter_by(medium=itemmedium)
#             queryStarted = True
#         else:
#             queryresult = queryresult.filter(Movie.medium.like(looking_for))
#             # queryresult = queryresult.filter_by(medium=itemmedium)
#
#     itemtext = searchitems['text']
#     if itemtext != '':
#         if queryStarted == False:
#             queryresult = Movie.query.filter_by(titleLocal=itemtext)
#             queryStarted = True
#         else:
#             queryresult = queryresult.filter_by(titleLocal=itemtext)
#
#     itemyear = searchitems['year']
#     if itemyear != '':
#         if queryStarted == False:
#             queryresult = Movie.query.filter_by(year=itemyear)
#             queryStarted = True
#         else:
#             queryresult = queryresult.filter_by(year=itemyear)
#
#     itemdirector = searchitems['director']
#     if itemdirector != '':
#         looking_for = '%{0}%'.format(itemdirector)
#         dir = Director.query.filter(Director.name.like(looking_for)).first()
#         dirid = dir.id
#         if queryStarted == False:
#             queryresult = Movie.query.filter_by(directors=dirid)
#             queryStarted = True
#         else:
#             queryresult = queryresult.filter_by(directors=dirid)
#     found = queryresult.all()
#     return found
#
#
# def insertMovieData(inputMovieId, inputTitle='', medium='', source='', place=''):
#     '''insert data from input into db
#     Data from Input (manual or csv) has structure:
#     imdbId 7 char obligatory
#     title (local title) optional
#     medium optional
#     source otpional
#     If imdbId not found in db, then add item to db
#     else add(modify) items already present
#     '''
#     dbMovie = None
#     try:
#         dbMovie = searchDb(inputMovieId)
#     except:
#         pass
#     if dbMovie == None:
#         addManMovieToDb(inputMovieId, inputTitle, medium, source, place)
#     else:
#         updateMovieManual(inputMovieId, inputTitle, medium, source, place)
#
#
# def searchDb(movieId):
#     ''' search local db for movie,
#     return set of data if found, or None if not found'''
#     found = Movie.query.filter_by(imdbId= movieId).first()
#     return found
#
#
# def searchDirectorDb(peopleId):
#     ''' search local db for movie,
#     return set of data if found, or None if not found'''
#     found = None
#     try:
#         found = Director.query.filter_by(peopleImdbId= peopleId).first()
#     except:
#         pass
#     return found
#
#
# def addManMovieToDb(inputMovieId, inputTitle='', medium='', source='', place=''):
#     '''
#     first search local imdb data for item, extract infos about
#     movie, director, rating
#     then insert new data set to db
#     '''
#
#     # get data from imdb tsv
#     imdbData = tsv.getMovieData(inputMovieId)
#     titleImdb=''
#     titleOrig=''
#     year = ''
#     director = ''
#     # prepare data for
#     length = 0
#     if imdbData != None:
#         length = imdbData[0]
#         titleImdb = imdbData[1]
#         if len(imdbData) > 2:
#             titleOrig = imdbData[2]
#             if len(imdbData) > 3:
#                 year = imdbData[3]
#
#     newMovie = Movie(imdbId=inputMovieId,
#                      titleImdb=titleImdb,
#                      titleOrig=titleOrig,
#                      titleLocal=inputTitle,
#                      medium = medium,
#                      year = year,
#                      linelength = length,
#                      place = place,
#                      source = source)
#     dirData = tsv.getMovieDirector(inputMovieId)
#     if dirData != None:
#         directorId = dirData
#         dirInDb = searchDirectorDb(directorId)
#         if dirInDb == None:
#             dirName = tsv.getNameData(directorId)
#             director = Director(peopleImdbId=directorId, name=dirName)
#             db.session.add(director)
#         else:
#             director = dirInDb
#         newMovie.director = director
#
#     ratData = tsv.getMovieRating(inputMovieId)
#     if ratData != None:
#         try:
#             critic = Critic.query.filter_by(name='Imdb').first()
#             rat = Rating(movie_id=newMovie.id, critic_id=critic.id, value=ratData)
#             db.session.add(rat)
#         except:
#             pass
#     db.session.add(newMovie)
#     db.session.commit()
#
#
# def addManMovieWithoutIdToDb(inputTitle='', medium='-', source='', place=''):
#     '''
#     '''
#     newMovie = Movie(
#         imdbId='0000000',
#                      titleLocal=inputTitle,
#                      medium = medium,
#                      place=place,
#                      source = source)
#     db.session.add(newMovie)
#     db.session.commit()
#
#
# def updateMovieWithoutIDWithImdb(movie, imdbid, commit=True):
#
#     # search imdb for movie
#     # get data from imdb tsv
#     imdbData = tsv.getMovieData(imdbid)
#     titleImdb=''
#     titleOrig=''
#     year = ''
#     director = ''
#     # prepare data for
#     length = 0
#     if imdbData != None:
#         length = imdbData[0]
#         titleImdb = imdbData[1]
#         if len(imdbData) > 2:
#             titleOrig = imdbData[2]
#             if len(imdbData) > 3:
#                 year = imdbData[3]
#
#     movie.imdbId=imdbid
#     movie.titleImdb=titleImdb
#     movie.titleOrig=titleOrig
#     movie.year = year
#     movie.linelength = length
#     dirData = tsv.getMovieDirector(imdbid)
#     if dirData != None:
#         directorId = dirData
#         dirInDb = searchDirectorDb(directorId)
#         if dirInDb == None:
#             dirName = tsv.getNameData(directorId)
#             director = Director(peopleImdbId=directorId, name=dirName)
#             db.session.add(director)
#         else:
#             director = dirInDb
#         movie.director = director
#
#     if commit:
#         db.session.commit()
#
#
# def updateMovieManual(movieId, inputTitle, medium, source, place):
#
#     found = Movie.query.filter_by(imdbId= movieId).first()
#     found.titleLocal = inputTitle
#     found.medium = medium
#     found.source = source
#     found.place = place
#     db.session.commit()
#
#
# def updateMovieWithTsv(movieId):
#
#     found = Movie.query.filter_by(imdbId=movieId).first()
#
#     tsvLengthNew = 0
#     tsvLengthOld = found.linelength
#     imdbData = tsv.getMovieData(movieId)
#     if imdbData != None:
#         tsvLengthNew = imdbData[0]
#
#     if tsvLengthNew > tsvLengthOld:
#         # titleImdb = ''
#         # titleOrig = ''
#         # year = ''
#         # director = ''
#         # # prepare data for
#         # length = imdbData[0]
#         titleImdb = imdbData[1]
#         found.titleImdb = titleImdb
#         if len(imdbData) > 2:
#             titleOrig = imdbData[2]
#             found.titleOrig = titleOrig
#             if len(imdbData) > 3:
#                 year = imdbData[3]
#                 found.year = year
#
#         db.session.commit()
#
# def deleteMovie(movieid):
#     obj = Movie.query.filter_by(id=movieid).first()
#     print(obj)
#     db.session.delete(obj)
#     db.session.commit()
#
# def updateMovie(movieid, form):
#     '''
#     movie without imdbId can get imdbId,
#     rest can get new medium (bought dvd) or user rating
#     :param movieid: db id
#     :param form: UpdateMovieForm to extract input data
#     '''
#     obj = Movie.query.filter_by(id=movieid).first()
#     imdbId = form.imdbid.data
#
#     ownRatingNew = form.ownrating.data
#     jd = Critic.query.filter_by(name='JD').first()
#     ownRatingOldObj = getRatingForMovie(obj, jd)
#     if ownRatingOldObj != None:
#         ownRatingOld = ownRatingOldObj.value
#     else:
#         ownRatingOld = None
#     if(ownRatingNew != ownRatingOld) and (ownRatingNew != ''):
#         if(ownRatingOldObj == None):
#             newRating = Rating(movie_id=obj.id, critic_id=jd.id, value=ownRatingNew)
#             # rat = Rating(movie_id=newMovie.id, critic_id=critic.id, value=ratData)
#             db.session.add(newRating)
#         else:
#             ownRatingOldObj.value = ownRatingNew
#
#     oldTitle = obj.titleLocal
#     newTitle = form.localname.data
#     if newTitle != oldTitle:
#         obj.titleLocal = newTitle
#
#     oldMedium = obj.medium
#     newMedium = form.medium.data
#     if newMedium != oldMedium:
#         obj.medium = newMedium
#
#     newplace = form.place.data
#     oldplace = obj.place
#     if newplace != oldplace:
#         obj.place = newplace
#
#     oldImdb = obj.imdbId
#     if oldImdb == '' or oldImdb == '0000000':
#         if imdbId != '' and imdbId != '0000000':
#             updateMovieWithoutIDWithImdb(obj, imdbId, commit=False)
#     db.session.commit()
#
# def updateCritic(criticid, form):
#     obj = Critic.query.filter_by(id=criticid).first()
#     name = form.name.data
#     url = form.url.data
#     maxVal = form.maxval.data
#     obj.name = name
#     obj.url = url
#     obj.maxVal = maxVal
#     db.session.commit()
#
#
#
# def getRatingForMovie(movieobj, criticobj):
#     object = None
#     try:
#         ownRatings = Rating.query.filter_by(critic_id=criticobj.id)
#         rating = ownRatings.filter_by(movie_id=movieobj.id).first()
#         object = rating
#     except:
#         pass
#     return object
#
# def getJdRatingForMovie(movieobj):
#     ownRating = None
#     try:
#         jd = Critic.query.filter_by(name='JD').first()
#         ownRatingObj = getRatingForMovie(movieobj, jd)
#         if ownRatingObj != None:
#             ownRating = ownRatingObj.value
#     except:
#         pass
#     return ownRating
#
#
