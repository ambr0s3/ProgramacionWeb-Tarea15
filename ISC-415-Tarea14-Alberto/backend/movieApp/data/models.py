from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))    
    poster = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='movie',
                                lazy='dynamic')

    def __init__(self, id, name, description, poster):
        self.id = id
        self.name = name
        self.description = description
        self.poster = poster

    def serialize(self):
        return {
            "id": self.id,
            "title": self.name,
            "description": self.description,
            "poster": self.poster,
            "reviews": [review.serialize() for review in self.reviews.all()]
        }

    def __repr__(self):
        return '<Movie %r>' % (self.name)


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    description = db.Column(db.String(100))
    rating = db.Column('rating', db.Integer)
    user = db.Column(db.String(100))
    device_id = db.Column(db.String(100))

    def serialize(self):
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "description": self.description,
            "rating": self.rating,
            "user": self.user,
            "device_id": self.device_id
        }

    def __init__(self, movie_id, description, rating, user, device_id):
        self.movie_id = movie_id
        self.description = description
        self.rating = rating
        self.user = user
        self.device_id = device_id

    def __repr__(self):
        return '<Review %r %r>' % (self.description, self.rating)
