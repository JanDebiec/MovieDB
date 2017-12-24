from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])

from config import Config

import imdbif.search as ims
from app import create_app, db
from app.models import Movie, Role, People, Director


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

class TestSicarioToDb:
    def setup(self):
        print("setup      class:TestSicarioToDb, fixture test method")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        print("teardown      class:TestSicarioToDb")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setup_class(self):
        self._inst = ims.SearchImdb()
        self._film = self._inst.getMovie(3397884)
        print("\nsetup class      class: %s, fixture test class" %self.__name__)

    def teardown_class(self):
        print("teardown class      class: %s" % self.__name__)


    def testMovieDirector(self):
        # coppola = Director(name='Coppola')
        imdbId, name = self._inst.getDirectorDetailsForDb(self._film)
        title = self._inst.getFilmTitle(self._film)
        sicario = Movie(titleImdb=title)
        denis = Director(name=name)
        sicario.director = denis
        assert 2 == 2
