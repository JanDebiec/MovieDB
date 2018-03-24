from pytest import fixture, mark
import sys
from bs4 import BeautifulSoup
sys.path.extend(['/home/jan/project/movie_db'])
from app import create_app, db
from app.mod_db.models import Movie, Role, People, Director, Rating, Critic
# import app.mod_db.controllers as dbc
import app.mod_db.functions as dbf
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

    def test_arr_count(self):
        count = mc.get_critics_count(self.arrival_soup)
        assert 52 == count

    def test_arr_ratings(self):
        count, list_ = mc.get_ratings_list(self.arrival_soup)
        assert 52 == count
        assert 52 == len(list_)

class TestMcIntoDb:
    def setup(self):
        print("setup method, class: TestMcIntoDb, fixture test method")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        sic = Movie(titleImdb='Sicario')
        db.session.add(sic)
        arr = Movie(titleImdb='Arrival')
        db.session.add(arr)
        db.session.commit()

    def teardown(self):
        print("teardown method class: TestMcIntoDb")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def setup_class(self):
        with open('input_data/mc_arrival.html', 'rb') as f:
            self.arrival_html = f.read()
        with open('input_data/mc_sicario.html', 'rb') as f:
            self.sicario_html = f.read()
        self.sicario_soup = BeautifulSoup(self.sicario_html, 'html.parser')
        self.arrival_soup = BeautifulSoup(self.arrival_html, 'html.parser')
        print("\nsetup class      class: %s, fixture test class" % self.__name__)

    def teardown_class(self):
        print("\nteardown class      class: %s" % self.__name__)

    def test_insert_sic(self):
        sic = Movie.query.filter_by(titleImdb='Sicario').first()
        sic_id = sic.id

        count, list_ = mc.get_ratings_list(self.sicario_soup)
        for item in list_:
            name = '{} {}'.format(item.author, item.source)
            url = 'http://www.metacritic.com/critic/{}?filter=movies'.format(item.author)
            maxVal = 100.0
            crit = Critic(name=name, url=url, maxVal=maxVal)
            crit_id = dbf.add_critic(crit)
            rat = Rating(sic_id, critic_id=crit_id, value=item.rating)
            db.session.add(rat)
        db.session.commit()

        critics = Critic.query.all()
        count_critics = len(critics)
        assert 48 == count_critics

        ratings = Rating.query.all()
        count_ratings = len(ratings)
        assert 48 == count_ratings

    def test_insert_arr(self):
        arr = Movie.query.filter_by(titleImdb='Arrival').first()
        arr_id = arr.id

        count, list_ = mc.get_ratings_list(self.arrival_soup)
        for item in list_:
            name = '{} {}'.format(item.author, item.source)
            url = 'http://www.metacritic.com/critic/{}?filter=movies'.format(item.author)
            maxVal = 100.0
            crit = Critic(name=name, url=url, maxVal=maxVal)
            crit_id = dbf.add_critic(crit)
            rat = Rating(arr_id, critic_id=crit_id, value=item.rating)
            db.session.add(rat)
        db.session.commit()

        critics = Critic.query.all()
        count_critics = len(critics)
        assert 52 == count_critics

        ratings = Rating.query.all()
        count_ratings = len(ratings)
        assert 52 == count_ratings

    def test_insert_arr_sic(self):
        arr = Movie.query.filter_by(titleImdb='Arrival').first()
        arr_id = arr.id

        dbf.insert_rating_for_movie_from_html(arr_id, self.arrival_html)

        sic = Movie.query.filter_by(titleImdb='Sicario').first()
        sic_id = sic.id

        dbf.insert_rating_for_movie_from_html(sic_id, self.sicario_html)

        critics = Critic.query.all()
        count_critics = len(critics)
        assert 76 == count_critics

        ratings = Rating.query.all()
        count_ratings = len(ratings)
        assert 100 == count_ratings

class TestNameConverter:

    def test_one_word(self):
        input_name = 'Sicario'
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = 'sicario'
        assert mc_name == reference_name

    def test_two_words(self):
        input_name = 'The Godfather'
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = 'the-godfather'
        assert mc_name == reference_name

    def test_three_words(self):
        input_name = 'I kill Giants'
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = 'i-kill-giants'
        assert mc_name == reference_name

    def test_name_with_dot_end(self):
        input_name = 'Robert Yannis Jr.'
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = 'robert-yannis-jr'
        assert mc_name == reference_name

    def test_name_with_dot_middle(self):
        input_name = 'Dr.A.A. Names'
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = 'draa-names'
        assert mc_name == reference_name

    def test_name_with_apo_middle(self):
        input_name = "Dr.A.A. O'Names"
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = 'draa-onames'
        assert mc_name == reference_name

    def test_space_odysee(self):
        input_name = "2001: A Space Odyssey"
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = '2001-a-space-odyssey'
        assert mc_name == reference_name

    def test_heil_caesar(self):
        input_name = "Hail, Caesar!"
        mc_name = mc.convert_name_to_mc(input_name)
        reference_name = 'hail-caesar!'
        assert mc_name == reference_name



# No pageviews found for black-cat,-white-cat
# No pageviews found for o-brother,-where-art-thou?