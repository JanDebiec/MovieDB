from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])
from app import create_app, db
from app.mod_db.models import Movie, Role, People, Director, Rating, Critic
import app.mod_db.controllers as dbc

from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestAppDb:
    def setup(self):
        print("setup method, class: TestAppDb, fixture test method")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        print("teardown method class: TestAppDb")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setup_class(self):
        print("\nsetup class      class: %s, fixture test class" % self.__name__)

    def teardown_class(self):
        print("teardown class      class: %s" % self.__name__)

    def test_1(self):
        value = 2
        assert 2 == value

    def test_add_first_movie(self):
        an = Movie(titleImdb='Apocalypse Now')
        db.session.add(an)
        db.session.commit()
        movies = Movie.query.all()
        c = len(movies)
        assert c == 1


    def test_add_two_movies(self):
        an = Movie(titleImdb='Apocalypse Now')
        sic = Movie(titleImdb='Sicario')
        db.session.add(an)
        db.session.add(sic)
        db.session.commit()
        movies = Movie.query.all()
        c = len(movies)
        assert c == 2


    def test_add_two_roles(self):
        an = Movie(titleImdb='Apocalypse Now')
        sic = Movie(titleImdb='Sicario')
        kurz = Role(characterName='Kurz', film=an)
        willard = Role(characterName='Willard', film=an)
        db.session.add(an)
        db.session.add(sic)
        db.session.add(kurz)
        db.session.add(willard)
        db.session.commit()
        movies = Movie.query.all()
        roles = Role.query.all()
        c = len(roles)
        assert c == 2

    def test_add_query_two_roles(self):
        an = Movie(titleImdb='Apocalypse Now')
        sic = Movie(titleImdb='Sicario')
        kurz = Role(characterName='Kurz', film=an)
        willard = Role(characterName='Willard', film=an)
        db.session.add(an)
        db.session.add(sic)
        db.session.add(kurz)
        db.session.add(willard)
        db.session.commit()
        m = Movie.query.get(1)
        roles = m.roles.all()
        c = len(roles)
        assert c == 2

    def test_add_two_roles_peoples(self):
        an = Movie(titleImdb='Apocalypse Now')
        sic = Movie(titleImdb='Sicario')
        marlon = People(name='Marlon')
        sheen = People(name='Scheen')
        kurz = Role(characterName='Kurz', film=an, actor=marlon)
        willard = Role(characterName='Willard', film=an, actor=sheen)
        db.session.add(marlon)
        db.session.add(sheen)
        db.session.add(an)
        db.session.add(sic)
        db.session.add(kurz)
        db.session.add(willard)
        db.session.commit()
        m = People.query.get(1)
        roles = m.roles.all()
        c = len(roles)
        assert c == 1
        name = roles[0].characterName
        assert name == 'Kurz'

    def test_add_director(self):
        an = Movie(titleImdb='Apocalypse Now')
        sic = Movie(titleImdb='Sicario')
        marlon = People(name='Marlon')
        sheen = People(name='Scheen')
        coppola = Director(name='Coppola')
        kurz = Role(characterName='Kurz')
        kurz.film = an
        kurz.actor = marlon
        willard = Role(characterName='Willard', film=an, actor=sheen)
        an.director = coppola
        db.session.add(marlon)
        db.session.add(sheen)
        db.session.add(coppola)
        db.session.add(an)
        db.session.add(sic)
        db.session.add(kurz)
        db.session.add(willard)
        db.session.commit()

        f = Movie.query.get(1)
        dir = f.director.name
        assert dir == 'Coppola'

    def test_own_critics(self):
        an = Movie(titleImdb='Apocalypse Now')
        sic = Movie(titleImdb='Sicario')
        marlon = People(name='Marlon')
        sheen = People(name='Scheen')
        coppola = Director(name='Coppola')
        kurz = Role(characterName='Kurz')
        kurz.film = an
        kurz.actor = marlon
        jd = Critic(name='JD', maxVal=5.0)
        rat = Rating(value=5.0)
        rat.film = an
        rat.critic= jd
        rats = Rating(value=4.5)
        rats.film = sic
        rats.critic = jd
        willard = Role(characterName='Willard', film=an, actor=sheen)
        an.director = coppola
        db.session.add(marlon)
        db.session.add(sheen)
        db.session.add(coppola)
        db.session.add(an)
        db.session.add(sic)
        db.session.add(kurz)
        db.session.add(willard)
        db.session.add(rat)
        db.session.add(rats)
        db.session.commit()
        # TODO check ratings

        f = Movie.query.get(1)
        print(type(f))
        dir = f.director.name
        print(dir)
        rq = Rating.query
        # rq = Rating.query.filter_by(critic_id='JD')
        r = rq.all()
        print(type(r))
        print(len(r))
        print(r)
        # rjd = rq.filter_by(movie_id='0')
        # print(rjd)
        # val = r.value
        # assert val == 5.0
        # m = r.movie_id
        # print('movie id = {}'.format(m))

