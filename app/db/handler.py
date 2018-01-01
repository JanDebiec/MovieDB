def insertMovieData(inputMovieId, inputTitle='', medium='', source=''):
    '''insert data from input into db
    Data from Input (manual or csv) has structure:
    imdbId 7 char obligatory
    title (local title) optional
    medium optional
    source otpional
    If imdbId not found in db, then add item to db
    else add(modify) items already present
    '''
    dbMovie = searchDb(inputMovieId)
    if dbMovie == None:
        addMovieToDb(inputMovieId, inputTitle, medium, source)
    else:
        updateMovieInDb()


def searchDb(movieId):
    ''' search local db for movie,
    return set of data if found, or None if not found'''
    return None

def addMovieToDb(inputMovieId, inputTitle='', medium='', source=''):
    '''
    first search local imdb data for item, extract infos about
    movie, director, rating
    then insert new data set to db
    '''
    pass

def updateMovieInDb():
    pass