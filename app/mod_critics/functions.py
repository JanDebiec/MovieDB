from math import sqrt
from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic, Rating
from config import Config


class Comparison():
    def __init__(self, nameA, nameB):
        self.nameA = nameA
        self.nameB = nameB
        self.sharedFlags = {}
        self.sharedRatings = {}
        self.ratingsA = {}
        self.countA = 0
        self.ratingsB = {}
        self.countB = 0

    def findCommonRatings(self):
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
        self.ratingsA = getRatingsFromCritic(self.nameA)
        self.countA = len(self.ratingsA)
        self.ratingsB = getRatingsFromCritic(self.nameB)
        self.countB = len(self.ratingsB)
        # shared = {}
        for item in self.ratingsA:
            if item in self.ratingsB:
                self.sharedFlags[item] = 1
        # create new dict: key=id, value=tuple with both ratings


    def calcCompare(self):
        ''' input: two lists of ratings
        steps:
        1. find common ratings
        2. normalize to 100
        3. calc
        4. normalize to movie count'''
        shared = self.findCommonRatings()
        return len(shared)

def getRatingsFromCritic(criticName):
    ''' return the list of ratings for the critic '''
    criticobj = Critic.query.filter_by(name=criticName).first()
    # ratings = Rating.query.filter_by(critic_id=criticobj.id).all()
    ratings = Rating.query.filter_by(critic_id=criticobj.id).order_by(Rating.movie_id.asc()).all()
    ratingDict = {}
    # create dict: key = movie.id, value normalized rating
    maxVal = criticobj.maxVal
    for rating in ratings:
        movieid = rating.movie_id
        value = rating.value
        valNorm = normalizeRating(value, maxVal)
        # valNorm = value * Config.MAX_VAL_NORM / maxVal
        ratingDict[movieid] = valNorm

    return ratingDict

def normalizeRating(rating, maxVal):
    '''normalize (extend to 100) the rating '''
    valNorm = rating * Config.MAX_VAL_NORM / maxVal
    return valNorm
