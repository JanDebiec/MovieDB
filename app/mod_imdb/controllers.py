import os
import sys
from flask import Blueprint, render_template, flash, redirect, url_for
from enum import Enum
import helper

mod_imdb = Blueprint('imdb', __name__, url_prefix='/mod_imdb')


movieBasicsFile = 'imdbif/title_basics.tsv'
# movieBasicsFile = 'app/import_tsv/title_basics.tsv'
nameBasicsFile = 'imdbif/name_basics.tsv'
# nameBasicsFile = 'app/import_tsv/name_basics.tsv'
movieDirectorFile = 'imdbif/title_crew.tsv'
# movieDirectorFile = 'app/import_tsv/title_crew.tsv'

class EMovieBasics(Enum):
    movieId = 0
    titleTyp = 1
    imdbTitle = 2
    originTitle = 3
    startYear = 5
    runTimeMin = 7

class EMovieDirector(Enum):
    movieId = 0
    director = 1

class EPerson(Enum):
    nameId = 0
    nameText = 1

def getMovieData(movieId):
    ''' search title_basics.tsv for movie
    return list > 0 if movie found
    items:
    tconst	titleType	primaryTitle	originalTitle	isAdult
    startYear	endYear	runtimeMinutes	genres
    '''
    try:
        line = findLineWithId(movieBasicsFile ,movieId)
        length = len(line)
        if length > 0:
            values = line.split('\t')
            imdbTitle = values[EMovieBasics.imdbTitle.value]
            origTitle = values[EMovieBasics.originTitle.value]
            year = values[EMovieBasics.startYear.value]
            runTime = values[EMovieBasics.runTimeMin.value]
            # return (imdbTitle, origTitle, year, runTime)
            return (length, imdbTitle, origTitle, year )
        else:
            return None
    except:
        return None


def getMovieDirector(movieId):
    ''' search title_crew.tsv for movie
    return list > 0 if person found
    items:
    tconst	directors	writers
    '''
    director = None
    line = findLineWithId(movieDirectorFile ,movieId)
    if len(line) > 0:
        values = line.split('\t')
        crew = values[EMovieDirector.director.value]
        if len(crew) > 2:
            director = crew[2:]
        return director

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
        name = values[EPerson.nameText.value]
        return name
    else:
        return None

def findLineWithId(filename, matchId, delimiter='\t', quiet=True):
    '''binary search in TSV files from IMDB'''
    try:
        counter = 0
        helperCounter = 1
        lineLengthInBytes = 1
        start = 0
        lastId = ''
        lineId = ''
        pwd = os.getcwd()
        if quiet != True:
            print(pwd , filename)
        end = os.path.getsize(filename)
        endBinary = "{0:b}".format(end)
        maxLoopCount = len(endBinary)
        # with helper.ManagedFile(filename) as fptr:
        with helper.ManagedUtfFile(filename) as fptr:

            while (start < end) and (counter < (maxLoopCount + 4)):
                lastId = lineId
                pos = start + ((end - start) / 2)

                fptr.seek(pos)
                fptr.readline()
                line = fptr.readline()
                lineLength = len(line)
                if counter == 0:
                    lineLengthInBits = "{0:b}".format(lineLength)
                    lineLengthInDigits = len(lineLengthInBits)
                values = line.split(sep=delimiter)
                firstValue = values[0]
                lineId = firstValue[2:]# ignore the first 2 chars
                if quiet != True:
                    print('lineId {} length {} start {} end {}'.format(lineId, lineLength, start, end))
                counter = counter + 1
                if matchId == lineId:
                    if quiet != True:
                        print("counter = {0} / {1}".format(counter, maxLoopCount))
                    return line
                elif matchId > lineId:
                    # newer dirty trick, from the near of the match, search linear, because of various line length
                    if maxLoopCount - counter < lineLengthInDigits + 6:
                        while lineId < matchId:
                            line = fptr.readline()
                            values = line.split(sep=delimiter)
                            firstValue = values[0]
                            lineId = firstValue[2:]  # ignore the first 2 chars
                            counter = counter + 1
                            if matchId == lineId:
                                if quiet != True:
                                    print("counter = {0} / {1}".format(counter, maxLoopCount))
                                return line
                    else:
                        start = fptr.tell()
                        if start > end:
                            end = start + 1
                else:
                    end = fptr.tell()
            if quiet != True:
                print("counter = {}, max = {}".format(counter, maxLoopCount))
            return []
    except:
        print("Oops!", sys.exc_info()[0], "occured.")
        return []

