from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])
import db.db as db

dbFileName = '../userdata/movieTestdb.sqlite'

tableMoviesStruct = \
    [('movies','imdbID','INTEGER'),
    ('movies','imdb_title','TEXT',''),
    ('movies','orig_title','TEXT',''),
    ('movies','local_title','TEXT',''),
    ('movies','medium','TEXT','no'),
    ('movies','blob','BLOB',''),
    ]

class TestUserDB:
    def setup(self):
        print("setup      class:TestUserDB, fixture test method")
        # self.inp = inputFrame.Input()

    def teardown(self):
        print("teardown      class:TestUserDB")

    def setup_class(self):
        print("\nsetup class      class: %s, fixture test class" % self.__name__)
        self._datab = db.UserDB(dbFileName)

    def teardown_class(self):
        print("teardown class      class: %s" % self.__name__)

    def test_construct(self):
        datab = db.UserDB(dbFileName)

    def test_constructTable(self):
        self._datab.constructTable(tableMoviesStruct)

#class TestUserDB:
