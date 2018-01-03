from pytest import fixture, mark
import sys
import csv
sys.path.extend(['/home/jan/project/movie_db'])
from app import create_app, db
from app.mod_db.models import Movie, Role, People, Director
import app.mod_db.controllers as dbc

from config import Config

import helper as h
import app.import_tsv as tsv

testFile = 'test/testInput.csv'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestAppDbModule:
    def setup(self):
        print("setup method, class: TestAppDbModule, fixture test method")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        print("teardown method class: TestAppDbModule")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setup_class(self):
        print("\nsetup class      class: %s, fixture test class" % self.__name__)

    def teardown_class(self):
        print("teardown class      class: %s" % self.__name__)

    def test_add_two_movies(self):
        dbc.addManMovieToDb(inputMovieId='0073802', inputTitle='Three Days of the Condor', medium='DVDR')
        dbc.addManMovieToDb(inputMovieId='1663202', inputTitle='The Revenant', medium='DVD')
        movies = Movie.query.all()
        c = len(movies)
        assert c == 2
        found = dbc.searchDb('0073802')
        assert found != None
        notfound = dbc.searchDb('0000000')
        print(type(notfound))
        assert notfound == None

    def testCsvInput(self):
        ''' first version to show the functionality'''
        with h.ManagedUtfFile(testFile) as f:
            csvReader = csv.reader(f)
            count = 0
            data = False
            for row in csvReader:
                if data == False:
                    data = True
                else:
                    if len(row) > 0:
                        count = count + 1
                        movieId = row[0]
                        (imdbID, EAN, title, titleorig, titlelocal, medium, nr, source) = \
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
                        print(imdbID, EAN, title, titleorig, titlelocal, medium, nr, source)
                        dbc.addManMovieToDb(inputMovieId=imdbID, inputTitle=titlelocal, medium=medium)

            movies = Movie.query.all()
            c = len(movies)
            assert c == count
