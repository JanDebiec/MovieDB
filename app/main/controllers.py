from flask import Blueprint, render_template, flash, redirect, url_for
# from app import current_app
from app import db
from app.mod_db.models import Movie, Role, People, Director

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET', 'POST'])
@mod_main.route('/index', methods=['GET', 'POST'])
def index():
    movies = Movie.query.all()
    amountMovie = len(movies)
    messageText = 'MovieDB with {} movies'.format(amountMovie)

    return render_template('index.html',
                           message=messageText,
                           title='Home')

