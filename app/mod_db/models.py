from app import db


# Define a base model for other database tables to inherit
class DbBase(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class Movie(DbBase):
    ''' as primary key used integer, not imdbId. Movie can not be listed in Imdb'''
    # columns
    # id = db.Column(db.Integer, primary_key=True)
    imdbId = db.Column(db.String(7))
    EAN = db.Column(db.String(13))
    titleImdb = db.Column(db.String(64)) # Imdb title
    titleOrig = db.Column(db.String(64)) # polish title for polish movies, or german, or ...
    titleLocal = db.Column(db.String(64)) # polish or german if bought in Pl (De)
    year = db.Column(db.String(4))
    medium = db.Column(db.String(8))
    source = db.Column(db.String(8))
    place = db.Column(db.String(8))
    linelength = db.Column(db.Integer)
    # external
    directors = db.Column(db.Integer, db.ForeignKey('director.id'))
    # relations
    roles = db.relationship('Role', backref='film', lazy='dynamic')
    ratings = db.relationship('Rating', backref='film', lazy='dynamic')

    def __init__(self, imdbId='',  titleImdb='', titleOrig='', titleLocal='',
                 directors='', year='', medium='', linelength=0, source='', place='', EAN=''):
        self.imdbId = imdbId
        self.titleImdb = titleImdb
        self.titleOrig = titleOrig
        self.titleLocal = titleLocal
        self.year = year
        self.medium = medium
        self.source = source
        self.place = place
        self.EAN = EAN
        self.directors = directors
        self.linelength = linelength


    def __repr__(self):
        return '<Movie imdbId={} titleLocal={} medium={}'.format(self.imdbId, self.titleLocal, self.medium)


class People(DbBase):
    # id = db.Column(db.Integer, primary_key=True)
    peopleImdbId = db.Column(db.String(7))
    name = db.Column(db.String(64))
    # relations
    roles = db.relationship('Role', backref='actor', lazy='dynamic')

    def __repr__(self):
        return '<People peopleId={peopleId} name={name}'.format(self.peopleId, self.name)


class Director(DbBase):
    # id = db.Column(db.Integer, primary_key=True)
    peopleImdbId = db.Column(db.String(7))
    name = db.Column(db.String(64))
    # relations
    movies = db.relationship('Movie', backref='director', lazy='dynamic')

    def __repr__(self):
        return '<Director peopleId={} name={}'.format(self.peopleImdbId, self.name)


class Role(DbBase):
    ''' as ids used intger id. Movie or People can not be listed in Imdb'''
    # id = db.Column(db.Integer, primary_key=True)
    characterName = db.Column(db.String(64))
    # external
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    def __repr__(self):
        return '<Role peopleId={peopleId} movieId={movieId}'.format(self.peopleId, self.movieId)


class Critic(DbBase):
    name = db.Column(db.String(64))
    url = db.Column(db.String(128))
    maxVal = db.Column(db.Float)
    simdistance = db.Column(db.Float)
    simperson = db.Column(db.Float)
    # relations
    # movies = db.relationship('Movie', backref='critic', lazy='dynamic')
    ratings = db.relationship('Rating', backref='critic', lazy='dynamic')

    def __init__(self, name='',  url='-', maxVal='100'):
        self.name = name
        self.url = url
        self.maxVal = maxVal

    def __repr__(self):
        return '<Critic name={name} maxVal={maxVal}'.format(self.name, self.maxVal)

class Rating(DbBase):
    value = db.Column(db.Float)
    # criticMaxValue = db.Column(db.Float)
    # external
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    critic_id = db.Column(db.Integer, db.ForeignKey('critic.id'))

    def __init__(self, movie_id='',  critic_id='-', value='0'):
        self.movie_id = movie_id
        self.critic_id = critic_id
        self.value = value

    def __repr__(self):
        return '<Rating movie={} critic={} Val={}'.format(self.movie_id, self.critic_id, self.value)
