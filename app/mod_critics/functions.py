from math import sqrt
from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic, Rating
from config import Config

def findCommonRatingsFor2Critics(criticAName, criticBName):
    ''' search through whole DB
    and find the movies with shared ratings
    from both critics
    result: dictionary: key movieId, value: tuple of both values
    TODO check if possible for more params (more critics)
    steps:
    1. find ratings for criticA, sorted on movieId
    2. find ratings for criticB, sorted on movieId
    3. find movies in both lists
    4. create the dict with values for both critics
    '''
    ratingDictA = getRatingsFromCritic(criticAName)
    ratingDictB = getRatingsFromCritic(criticBName)
    shared = {}
    for item in ratingDictA:
        if item in ratingDictB:
            shared[item] = 1
    # create new dict: key=id, value=tuple with both ratings
    pass

def getRatingsFromCritic(criticName):
    ''' return the list of ratings for the critic '''
    criticobj = Critic.query.filter_by(criticName=criticName)
    ratings = Rating.query.filter_by(critic_id=criticobj.id).all().order_by(Movie.id.asc())
    ratingDict = {}
    # create dict: key = movie.id, value normalized rating
    maxVal = criticobj.maxVal
    for rating in ratings:
        movieid = rating.movie_id
        value = rating.value
        valNorm = value * Config.MAX_VAL_NORM / maxVal
        ratingDict[movieid] = valNorm

    return ratingDict


def normalizeRating(rating, maxVal):
    '''normalize (extend to 100) the rating '''
    pass

def calc():
    ''' input: two lists of ratings
    steps:
    1. find common ratings
    2. normalize to 100
    3. calc
    4. normalize to movie count'''