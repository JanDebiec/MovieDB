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
        self.countShared = 0
        self.ratingsA = {}
        self.countA = 0
        self.ratingsB = {}
        self.countB = 0
        self.person = 0
        self.distance = 0

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
        for item in self.sharedFlags:
            # itemNr = item.key
            ratA = self.ratingsA[item]
            ratB = self.ratingsB[item]
            value = (ratA, ratB)
            self.sharedRatings[item] = value

    def compare(self):
        ''' input: two lists of ratings
        steps:
        1. find common ratings
        2. normalize to 100
        3. calc
        4. normalize to movie count'''
        self.findCommonRatings()
        self.countShared = len(self.sharedFlags)
        self.createDataForChart()
        self.sim_distance()
        self.sim_pearson()
        return self

    def createDataForChart(self):
        '''from shaaredRatings create a list with tuples
         with two values'''
        self.listForChart = []

        for item in self.sharedRatings:
            itemValue = self.sharedRatings[item]
            self.listForChart.append(itemValue)

    # def calc(self):
    #     ''' input: two lists of ratings
    #     steps:
    #     1. find common ratings
    #     2. normalize to 100
    #     3. calc
    #     4. normalize to movie count'''
    #     self.findCommonRatings()

    # Returns the Pearson correlation coefficient for p1 and p2
    def sim_pearson(self):
        # def sim_pearson(prefs, p1, p2):
        #     # Get the list of mutually rated items
        #     si = {}
        #     for item in prefs[p1]:
        #         if item in prefs[p2]: si[item] = 1
        #
        #     # if they are no ratings in common, return 0
        #     if len(si) == 0: return 0
        #
        # Sum calculations
        n = len(self.sharedRatings)

        # Sums of all the preferences
        sum1 = 0
        sum2 = 0
        sum1Sq = 0
        sum2Sq = 0
        pSum = 0
        for item in self.sharedRatings:
            itemValue = self.sharedRatings[item]
            rata = itemValue[0]
            ratb = itemValue[1]
            sum1 = sum1 + rata
            sum2 = sum2 + ratb

            # sum1 = sum([prefs[p1][it] for it in si])
            # sum2 = sum([prefs[p2][it] for it in si])

            # Sums of the squares
            sum1Sq = sum1Sq + pow(rata, 2)
            sum2Sq = sum2Sq + pow(ratb, 2)
            # sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
            # sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

            # Sum of the products
            pSum = pSum + (rata * ratb)
            # pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

        # Calculate r (Pearson score)
        num = pSum - (sum1 * sum2 / n)
        den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
        self.person = 0
        if den == 0:
            return  # person

        self.person = num / den

        # return person


    # Returns a distance-based similarity score for person1 and person2
    def sim_distance(self):
        # Get the list of shared_items
        # si = {}
        # for item in prefs[person1]:
        #     if item in prefs[person2]: si[item] = 1

        n = len(self.sharedRatings)

        # if they have no ratings in common, return 0
        if n == 0:
            self.distance = 0

        # Add up the squares of all the differences
        sum_of_squares = 0
        for item in self.sharedRatings:
            itemValue = self.sharedRatings[item]
            rata = itemValue[0]
            ratb = itemValue[1]
            sumofq = pow((rata - ratb),2)
            sum_of_squares = sum_of_squares + sumofq

        # sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
        #                       for item in prefs[person1] if item in prefs[person2]])
        sum_of_squares_norm = sum_of_squares/n
        dist =  1 / (1 + sqrt(sum_of_squares_norm))
        self.distance = dist



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
