import sys
import json
from flask import Blueprint, render_template, flash, redirect, url_for, request
from jinja2 import Template

from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic, Rating
from app.mod_db.forms import ManInputForm, EditCriticForm, CriticsListForm, SearchDbForm, SingleResultForm, EditMovieForm, DeleteMovieForm, ExploreForm, PageResultsForm

import app.mod_imdb.controllers as tsv
# import app.mod_critics.metacritics as mc

from app.mod_db.functions import *
from flask import current_app


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
        searchdir['place'] = form.place.data
        searchdir['director'] = form.director.data
        searchdir['rating'] = form.rating.data
        searchdir['critic'] = form.critic.data

        searchitems = json.dumps(searchdir)
        return redirect(url_for('database.pageresults', searchitems=searchitems))
        # if searchitems['amgrating'] =='':
        #     return redirect(url_for('database.pageresults', searchitems=searchitems))
        # else:
        #     return redirect(url_for('database.amgresults', searchitems=searchitems))

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
        form.place.data = movie.place
        form.localname.data = movie.titleLocal
        form.director.data = movie.director.name
    except:
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
        # pass
    return render_template('mod_db/delete.html',
                           title='Movie to delete',
                           moviemsg=movietxt,
                           form=form)

@mod_db.route('/maninput', methods=['GET', 'POST'])
def maninput():
    form = ManInputForm()
    if form.validate_on_submit():
        flash('Added Movie: Id={}, localName={}, medium={}'.format(
            form.imdbid.data, form.localname.data, form.medium.data
        ))
        insertMovieDataFromForm(form)
        # insertManualInput(form)
        return redirect('/index')
    return render_template('mod_db/maninput.html',
                           title='Manual Input',
                           form=form)




@mod_db.route('/edit/<movieid>', methods=['GET', 'POST'])
def edit(movieid):
    form = EditMovieForm()
    foundMessage = 'search'
    if form.validate_on_submit():
        try:
            if form.upgradeimdb.data == True:
                upgradeMovie(movieid, form)
            updateMovie(movieid, form)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())

        try:
            if form.upgrademc.data == True:
                updateMovieMetacrit(movieid, form)
            # updateMovie(movieid, form)
        except:
            current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())

        # movie = Movie.query.filter_by(id=movieid).first()
        # movietxt = movie
        # return redirect(url_for('database.edit', title='Movie to edit',
        #                    moviemsg=movietxt,
        #                    movie=movie,
        #                    form=form))
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
        current_app.logger.error('director not found', exc_info=sys.exc_info())
        # pass
    try:
        form.ownrating.data = getRatingValueForMovie(movie, 'JD')
    except:
        current_app.logger.error('ownrating not found', exc_info=sys.exc_info())
        # pass
    try:
        form.ratingAmg.data = getRatingValueForMovie(movie, 'AMG')
    except:
        current_app.logger.error('amg rating not found', exc_info=sys.exc_info())
        # pass
    try:
        mc_rating = getRatingValueForMovie(movie, 'MC')
        form.ratingMCvalue.data = mc_rating
        ratings = Rating.query.filter_by(movie_id=movie.id).all()
        ratings_count = len(ratings)
        form.ratingMCcount.data = ratings_count
    except:
        current_app.logger.error('mc rating not found', exc_info=sys.exc_info())
    return render_template('mod_db/edit.html',
                           title='Movie to edit',
                           moviemsg=movietxt,
                           movie=movie,
                           form=form)

@mod_db.route('/pageresults/<searchitems>', methods=['GET', 'POST'])
def pageresults(searchitems):
    form = PageResultsForm()
    # we need the results of search onSubmit too,
    # to update the medium and ratings
    searchdir = json.loads(searchitems)
    foundMovieList = searchInDb(searchdir)
    foundList = []
    resultCount = 0

    listMovieToDisplay = []
    if foundMovieList != None:
        listMovieToDisplay = convert_list_to_display(foundMovieList)


    # if activated, filter the results with amg rating
    itemcritic = searchdir['critic']
    if itemcritic != '':
        criticName = itemcritic
    itemrating = searchdir['rating']
    if itemrating != '':
        foundList = filterMoviesWithCriticRating(listMovieToDisplay, criticName, itemrating)
    else:
        foundList = listMovieToDisplay
    resultCount = len(foundList)
    if form.validate_on_submit():
        if request.method == 'POST':
            userinputs = request.form
            newdict = userinputs.to_dict()
            amount = len(newdict)
            # we do not know the amount of ratings or medium
            # we know only global size of input
            flagDbShouldCommit = False
            # extracting user ratings input
            inputOwnRating = []
            for i in range(resultCount):
                try:
                    pointerString = 'ownrat[{}]'.format(i)
                    rat = newdict[pointerString]
                    if rat != '':
                        flagDbShouldCommit = True
                    inputOwnRating.append(rat)
                except: # no more ratings
                    break
            # extracting amg ratings input
            inputAmRating = []
            for i in range(resultCount):
                try:
                    pointerString = 'amgrat[{}]'.format(i)
                    rat = newdict[pointerString]
                    if rat != '':
                        flagDbShouldCommit = True
                    inputAmRating.append(rat)
                except: # no more ratings
                    break
            # extracting user medium input
            inputMedium = []
            for i in range(resultCount):
                try:
                    pointerString = 'medium[{}]'.format(i)
                    med = newdict[pointerString]
                    if med != '' and med != '-':
                        flagDbShouldCommit = True
                    inputMedium.append(med)
                except: # no more medium input
                    break
            inputPlace = []
            for i in range(resultCount):
                try:
                    pointerString = 'place[{}]'.format(i)
                    plc = newdict[pointerString]
                    if plc != '' and plc != '-':
                        flagDbShouldCommit = True
                    inputPlace.append(plc)
                except: # no more medium input
                    break

            updateOwnerRatingInDb(foundMovieList, inputOwnRating)
            updateAmgRatingInDb(foundMovieList, inputAmRating)
            updateMediumInDb(foundMovieList, inputMedium)
            updatePlaceInDb(foundMovieList, inputPlace)
            if flagDbShouldCommit:
                db.session.commit()

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



def init_mc_db():
    # create the list of movies with JD or AMG ratings
    critic_jd = Critic.query.filter_by(name= 'JD').first()
    critic_mc =  Critic.query.filter_by(name= 'MC').first()
    JD_list = Rating.query.filter_by(critic_id=critic_jd.id).all()
    movie_dict = {}
    for rating in JD_list:
        movie = Movie.query.fiter_by(id=rating.movie_id)
        query = Rating.query.filter_by(movie_id=movie.id)
        mc_ratings = query.filter_by(critic_id= critic_mc.id)
        # check if mc content already saved in DB
        # if not
        #     load mc data and save in DB
        if len(mc_ratings) <= 0:
            movie_dict[rating.movie_id] = movie

    listWithRatings = list(movie_dict.values())
    for movie in listWithRatings:
         mc_name = mc.convert_name_to_mc(movie.titleImdb)
         html = mc.get_response(mc_name)
         insert_rating_for_movie_from_html(html, movie.id)

