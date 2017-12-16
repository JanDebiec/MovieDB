from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])

import imdbif.search as ims


# @fixture(scope='module')
# def creatInstance():
#     inst = ims.SearchImdb()
#     return inst
#
# def test_search_imdb_Sicario():
#     i = creatInstance()
#     films = i.searchMovie("Sicario")
#     assert len(films[1]) == 20
#
# def test_getSicario():
#     i = creatInstance()
#     film = i.getMovie(3397884)
#     assert film['title'] == 'Sicario'

class TestExtractSicarioInfos:

    def setup(self):
        print("setup      class:TestExtractInfosClass, fixture test method")
        # self.inp = inputFrame.Input()

    def teardown(self):
        print("teardown      class:TestExtractInfosClass")

    def setup_class(self):
        self._inst = ims.SearchImdb()
        self._film = self._inst.getMovie(3397884)
        sizeOfFilm = sys.getsizeof(self._film)
        sizeOfClass = sys.getsizeof(self)
        print('size of film = %s' % sizeOfFilm)
        print('size of class = %s' % sizeOfClass)

        print("\nsetup class      class: %s, fixture test class" %self.__name__)

    def teardown_class(self):
        print("teardown class      class: %s" % self.__name__)

    def test_title(self):
        title = self._inst.getFilmTitle(self._film)
        assert title == 'Sicario'

    def test_year(self):
        year = self._inst.getFilmYear(self._film)
        assert year == 2015

    def test_rating(self):
        year = self._inst.getFilmRating(self._film)
        assert year == 7.6

    def test_cast_whole(self):
        cast = self._inst.getFilmCast(self._film)
        size = len(cast)
        assert size == 101

    def test_cast_6(self):
        cast = self._inst.getFilmCast(self._film, 6)
        size = len(cast)
        assert size == 6

    def test_directorsList(self):
        list = self._inst.getFilmDirectors(self._film)
        assert len(list) == 1

    def test_directorID(self):
        directorID = self._inst.getFilmFirstDirectorID(self._film)
        assert directorID == '0898288'

    def test_directorName(self):
        directorName = self._inst.getFilmFirstDirectorName(self._film)
        assert directorName == 'Villeneuve, Denis'

    def test_getActorName(self):
        actorList = self._inst.getFilmCast(self._film,1)
        actor = actorList[0]
        actorId, actorName = self._inst.getPersonDetails(actor)
        assert actorId == '1289434'
        assert actorName == 'Blunt, Emily'

    def test_getActorRole(self):
        actorList = self._inst.getFilmCast(self._film, 1)
        actor = actorList[0]
        role = self._inst.getActorRole(actor)
        assert role == 'Kate Macer'
