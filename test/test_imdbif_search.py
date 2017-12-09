from pytest import fixture, mark
import sys
sys.path.extend(['/home/jan/project/movie_db'])

import imdbif.search as ims

# def test_found_one_result_should_be_list_with_one_movie(search_movie):
#     page = search_movie('od instituta do proizvodnje')
#     data = parser.parse(page)['data']
#     assert data == [
#         ('0483758', {'kind': 'short', 'title': 'Od instituta do proizvodnje', 'year': 1971})
#     ]

@fixture(scope='module')
def creatInstance():
    inst = ims.SearchImdb()
    return inst

def test_search_imdb_Sicario():
    i = creatInstance()
    films = i.searchMovie("Sicario")
    assert len(films[1]) == 20