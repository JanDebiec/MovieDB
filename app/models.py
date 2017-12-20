from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieId = db.Column(db.String(7), index=True)
    EAN = db.Column(db.String(13), index=True)
    titleImdb = db.Column(db.String(64), index=True)
    titleOrig = db.Column(db.String(64), index=True)
    titleLocal = db.Column(db.String(64), index=True)
    medium = db.Column(db.String(8), index=True)

    def __repr__(self):
        return '<Movie id={id} title={title} medium={medium}'.format(self.movieId, self.titleImdb, self.medium)