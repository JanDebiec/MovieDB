import helper
from enum import Enum

movieBasicsFile = 'imdbif/title_basics.tsv'
nameBasicsFile = 'imdbif/name_basics.tsv'
movieDirectorFile = 'imdbif/title_crew.tsv'

class MovieBasics(Enum):
    movieId = 0
    titleTyp = 1
    imdbTitle = 2
    originTitle = 3
    startYear = 5
    runTimeMin = 7

def getMovieData(movieId):
    ''' search title_basics.tsv for movie
    return list > 0 if movie found
    items:
    tconst	titleType	primaryTitle	originalTitle	isAdult
    startYear	endYear	runtimeMinutes	genres
    '''
    try:
        line = helper.findLineWithId(movieBasicsFile ,movieId)
        if len(line) > 0:
            values = line.split('\t')
            imdbTitle = values[MovieBasics.imdbTitle.value]
            origTitle = values[MovieBasics.originTitle.value]
            year = values[MovieBasics.startYear.value]
            runTime = values[MovieBasics.runTimeMin.value]
            # return (imdbTitle, origTitle, year, runTime)
            return (imdbTitle, origTitle, year, runTime)
        else:
            return None
    except:
        return None


class MovieDirector(Enum):
    movieId = 0
    director = 1

def getMovieDirector(movieId):
    ''' search title_crew.tsv for movie
    return list > 0 if person found
    items:
    tconst	directors	writers
    '''
    line = helper.findLineWithId(movieBasicsFile ,movieId)
    if len(line) > 0:
        values = line.split('\t')
        director = values[MovieDirector.director.value]
        return director
    else:
        return None

class PersonEnums(Enum):
    nameId = 0
    nameText = 1

def getNameData(personId):
    ''' search name_basics.tsv for person
    return list > 0 if person found
    items:
    nconst	primaryName	birthYear	deathYear
    primaryProfession	knownForTitles

    '''
    line = helper.findLineWithId(nameBasicsFile ,personId)
    if len(line) > 0:
        values = line.split('\t')
        name = values[PersonEnums.nameText.value]
        return name
    else:
        return None
