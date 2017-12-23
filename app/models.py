from app import db

class Movie(db.Model):
    ''' as primary key used integer, not imdbId. Movie can not be listed in Imdb'''
    # columns
    id = db.Column(db.Integer, primary_key=True)
    imdbId = db.Column(db.String(7))
    EAN = db.Column(db.String(13))
    titleImdb = db.Column(db.String(64)) # Imdb title
    titleOrig = db.Column(db.String(64)) # polish title for polish movies, or german, or ...
    titleLocal = db.Column(db.String(64)) # polish or german if bought in Pl (De)
    medium = db.Column(db.String(8))
    diskNr = db.Column(db.String(8))
    # external
    directors = db.Column(db.Integer, db.ForeignKey('director.id'))
    # relations
    roles = db.relationship('Role', backref='film', lazy='dynamic')

    def __repr__(self):
        return '<Movie id={id} title={title} medium={medium}'.format(self.imdbId, self.titleImdb, self.medium)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peopleImdbId = db.Column(db.String(7))
    name = db.Column(db.String(64))
    # relations
    roles = db.relationship('Role', backref='actor', lazy='dynamic')

    def __repr__(self):
        return '<People peopleId={peopleId} name={name}'.format(self.peopleId, self.name)

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peopleImdbId = db.Column(db.String(7))
    name = db.Column(db.String(64))
    # relations
    movies = db.relationship('Movie', backref='director', lazy='dynamic')

    def __repr__(self):
        return '<Director peopleId={peopleId} name={name}'.format(self.peopleId, self.name)

class Role(db.Model):
    ''' as ids used intger id. Movie or People can not be listed in Imdb'''
    id = db.Column(db.Integer, primary_key=True)
    characterName = db.Column(db.String(64))
    # external
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    def __repr__(self):
        return '<Role peopleId={peopleId} movieId={movieId}'.format(self.peopleId, self.movieId)

# class Critic(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     url = db.Column(db.String(128))
#     maxVal = db.Column(db.Float)
#
#     def __repr__(self):
#         return '<Critic name={name} maxVal={maxVal}'.format(self.name, self.maxVal)
#
# class Rating(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     movieId = db.Column(db.String(7))
#     criticId = db.Column(db.Integer)
#     value = db.Column(db.Float)
#     criticMaxValue = db.Column(db.Float)
