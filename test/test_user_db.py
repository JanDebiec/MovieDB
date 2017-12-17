from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])
import db.db as db

dbFileName = '../userdata/movieTestdb6.sqlite'

tableName = 'movies'
tableMoviesStruct = \
    [('movies','imdbID','INTEGER'),
    ('movies','imdb_title','TEXT',''),
    ('movies','orig_title','TEXT',''),
    ('movies','local_title','TEXT',''),
    ('movies','medium','TEXT','no'),
    ('movies','blob','BLOB',''),
    ]

class TestConstructUserDB:
    def setup(self):
        print("setup      class:TestConstructUserDB, fixture test method")
        # self.inp = inputFrame.Input()

    def teardown(self):
        print("teardown      class:TestConstructUserDB")
        # self._datab.close()

    def setup_class(self):
        print("\nsetup class      class: %s, fixture test class" % self.__name__)
        # self._datab = db.UserDB(dbFileName)

    def teardown_class(self):
        print("teardown class      class: %s" % self.__name__)
        # self._datab.close()
        # tdb.dropTable(tableName)

    def test_constructTable(self):
        with db.UserDB(dbFileName) as tdb:
            tdb.constructTable(tableMoviesStruct)
            tdb.dropTable(tableName)


#class TestUserDB:
