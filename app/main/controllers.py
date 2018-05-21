from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user
# from app import current_app
from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic, Rating, User

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET', 'POST'])
@mod_main.route('/index', methods=['GET', 'POST'])
def index():
    movies = Movie.query.all()
    amountMovie = len(movies)
    directors = Director.query.all()
    amountDirectors = len(directors)
    critics = Critic.query.all()
    amountCritis = len(critics)
    ratings = Rating.query.all()
    amountRatings = len(ratings)
    messageText = 'MovieDB with: {} movies, {} directors, {} critics and {} ratings'.format(
        amountMovie,
        amountDirectors,
        amountCritis,
        amountRatings)

    return render_template('index.html',
                           message=messageText,
                           title='Home')

@mod_main.route('/ownrating', methods=['GET', 'POST'])
def ownrating():
    return render_template('/ownrating.html',
                           title='Criteria for own ratings')

