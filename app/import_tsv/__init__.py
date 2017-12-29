import os
import sys
import helper
from enum import Enum

movieBasicsFile = 'imdbif/title_basics.tsv'
# movieBasicsFile = 'app/import_tsv/title_basics.tsv'
nameBasicsFile = 'imdbif/name_basics.tsv'
# nameBasicsFile = 'app/import_tsv/name_basics.tsv'
movieDirectorFile = 'imdbif/title_crew.tsv'
# movieDirectorFile = 'app/import_tsv/title_crew.tsv'

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
        line = findLineWithId(movieBasicsFile ,movieId)
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
    line = findLineWithId(movieBasicsFile ,movieId)
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
    line = findLineWithId(nameBasicsFile ,personId)
    # line = helper.findLineWithId(nameBasicsFile ,personId)
    if len(line) > 0:
        values = line.split('\t')
        name = values[PersonEnums.nameText.value]
        return name
    else:
        return None

def findLineWithId(filename, matchId, delimiter='\t'):
    '''binary search in TSV files from IMDB'''
    try:
        counter = 0
        helperCounter = 1
        start = 0
        lastId = ''
        lineId = ''
        pwd = os.getcwd()
        print(pwd)
        end = os.path.getsize(filename)
        endBinary = "{0:b}".format(end)
        maxLoopCount = len(endBinary)
        # with helper.ManagedFile(filename) as fptr:
        with helper.ManagedUtfFile(filename) as fptr:

            while (start < end) and (counter < maxLoopCount):
                lastId = lineId
                pos = start + ((end - start) / 2)

                fptr.seek(pos)
                fptr.readline()
                line = fptr.readline()
                lineLength = len(line)
                values = line.split(sep=delimiter)
                firstValue = values[0]
                lineId = firstValue[2:]# ignore the first 2 chars
                # if debug == True:
                # print(lineId)
                counter = counter + 1
                if matchId == lineId:
                    return line
                elif matchId > lineId:
                    start = fptr.tell()
                else:
                    if lastId == lineId:
                        helperCounter = helperCounter + 1
                        end = fptr.tell() - helperCounter*lineLength
                        if start > end:
                            start = end - 1
                    else:
                        end = fptr.tell()
            # if debug:
            print("counter = {}".format(counter))
            return []
    except:
        print("Oops!", sys.exc_info()[0], "occured.")
        return []

