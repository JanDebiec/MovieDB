from pytest import fixture, mark
import sys
from bs4 import BeautifulSoup
sys.path.extend(['/home/jan/project/movie_db'])
from app import create_app, db
from app.mod_db.models import Movie, Role, People, Director, Rating, Critic
import app.mod_db.controllers as dbc
import app.mod_critics.tools as t
import app.mod_critics.metacritics as mc
import time
import collections



from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestMcDb:
    def setup(self):
        print("setup method, class: TestMcDb, fixture test method")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        print("teardown method,  class: TestMcDb")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setup_class(self):
        print("\nsetup_class      class: %s, fixture test class" % self.__name__)

    def teardown_class(self):
        print("teardown_class      class: %s" % self.__name__)

    def test_1(self):
        value = 2
        assert 2 == value

    def test_add_two_movies(self):
        arr = Movie(titleImdb='Arrival')
        sic = Movie(titleImdb='Sicario')
        db.session.add(arr)
        db.session.add(sic)
        db.session.commit()
        movies = Movie.query.all()
        c = len(movies)
        assert c == 2

    def test_add_two_movies_with_id(self):
        arr = Movie(imdbId= '2543164', titleLocal='Arrival')
        sic = Movie(imdbId='3397884' ,titleLocal='Sicario')
        db.session.add(arr)
        db.session.add(sic)
        db.session.commit()
        movies = Movie.query.all()
        c = len(movies)
        assert c == 2

class TestExtractSoup:
    def setup(self):
        self.sicario_soup = BeautifulSoup(self.sicario_html, 'html.parser')
        self.arrival_soup = BeautifulSoup(self.arrival_html, 'html.parser')
        print("setup method, class: TestExtractSoup, fixture test method")

    def setup_class(self):
        print("\nsetup class      class: %s, fixture test class" % self.__name__)
        with open('input_data/mc_arrival.html', 'rb') as f:
            self.arrival_html = f.read()
        with open('input_data/mc_sicario.html', 'rb') as f:
            self.sicario_html = f.read()

    def teardown_class(self):
        print("\nteardown class      class: %s" % self.__name__)

    def test_1(self):
        value = 2
        assert 2 == value

    def test_sic_count(self):
        count = mc.get_critics_count(self.sicario_soup)
        assert 48 == count

    def test_sic_ratings(self):
        count, list_ = mc.get_ratings_list(self.sicario_soup)
        assert 48 == count
        assert 48 == len(list_)

