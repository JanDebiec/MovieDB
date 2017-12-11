import sys
try:
    import imdb
except ImportError:
    print ('You bad boy!  You need to install the IMDbPY package!')
    sys.exit(1)

IMDB_AS = 'web'
IMDB_PARAMS = []
IMDB_KWDS = {}

class SearchImdb:
    def __init__(self):
        self._i = imdb.IMDb(IMDB_AS, *IMDB_PARAMS, **IMDB_KWDS)

    def searchMovie(self, title):
        results = None
        try:
            # Do the search, and get the results (a list of Movie objects).
            results = self._i.search_movie(title)
        except imdb.IMDbError as e:
            print ("Probably you're not connected to Internet.  Complete error report:")
            print (e)
            return (-1, results)
        count = len(results)
        return (count, results)

    def getMovie(self, imdbID):
        try:
            film = self._i.get_movie(imdbID)
        except imdb.IMDbError as e:
            print ("Probably you're not connected to Internet.  Complete error report:")
            print (e)
            return (None)
        return film

    def getFilmTitle(self, movie):
        return movie['title']

    def getFilmYear(self, movie):
        return movie['year']

    def getFilmRating(self, movie):
        return movie['rating']

    def getFilmDirectors(self, movie):
        return movie['director']

    def getFilmFirstDirector(self, movie):
        list = movie['director']
        return list[0]

    def getFilmFirstDirectorID(self, movie):
        list = movie['director']
        first = list[0]
        return first.personID

    def getFilmFirstDirectorName(self, movie):
        list = movie['director']
        first = list[0]
        return first.data['name']

    def getFilmCast(self, movie, amount = -1):
        cast = movie['cast']
        if amount < 0:
            return cast
        else:
            return cast[0:amount]

    def printFilmInfo(self,film):
        print('ID = {0}, title = {1}, data = {2} '.format(film.movieID, film['long imdb canonical title'], film.data))
        for people in film['cast'][0:6]:
            print('name {0}, role {1}'.format(people['name'], people.currentRole))

    def getPersonDetails(self, person):
        '''person should be class imdb.Person.Person'''
        personId = person.personID
        name = person.data['name']
        return (personId, name)

    def getActorRole(self, person):
        currentRole = person.currentRole.data['name']
        return currentRole


    def printResults(self, results):
        # Print the results.
        print('imdbID  ::               imdbURL                 ::     title')
        for movie in results:
            # print() '%s :: %s :: %s' % (movie.movieID,
            #                     self.i.get_imdbURL(movie),
            #                     movie['long imdb title'].encode(out_encoding, 'replace')))
            # print( '%s :: %s ' % movie.movieID, self.i.get_imdbURL(movie))
            # print( '%s ' % movie.smartCanonicalTitle)
            print( '{0}  ::  {1} '.format(movie.movieID, movie.data))

