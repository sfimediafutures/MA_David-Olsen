from crypt import methods
from datetime import timezone
from operator import ge
from platform import release
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS 
from features import get_image_features
from features import get_content



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'Hook this up to postgresql database'
db = SQLAlchemy(app)
CORS(app)

''' 
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Event: {self.description}'
    
    def __init__(self, description):
        self.description = description

'''

class Movie(db.Model):
    __tablename__ = 'Movie-data'

    title = db.Column(db.String, nullable=True)
    year = db.Column(db.String, nullable=True)
    rated = db.Column(db.String, nullable=True)
    released = db.Column(db.String, nullable=True)
    runtime = db.Column(db.String, nullable=True)
    genre = db.Column(db.String, nullable=True)
    director = db.Column(db.String, nullable=True)
    writer = db.Column(db.String, nullable=True)
    poster = db.Column(db.String, nullable=True)
    imdb_rating = db.Column(db.String, nullable=True)
    imdb_votes = db.Column(db.String, nullable=True)
    imdb_id = db.Column(db.String, nullable=False, primary_key=True)
    type = db.Column(db.String, nullable=False)
    saturation = db.Column(db.Float, nullable=False)
    brightness = db.Column(db.Float, nullable=False)
    entropy = db.Column(db.Float, nullable=False)
    sharpness = db.Column(db.Float, nullable=False)
    contrast = db.Column(db.Float, nullable=False)
    colorfulness = db.Column(db.Float, nullable=False)
    hex_0 = db.Column(db.String, nullable=False)
    hex_1 = db.Column(db.String, nullable=False)
    hex_2 = db.Column(db.String, nullable=False)
    hex_3 = db.Column(db.String, nullable=False)
    hex_4 = db.Column(db.String, nullable=False)


    
    def __init__(self, 
                title, 
                year, 
                rated, 
                released, 
                runtime, 
                genre, 
                director, 
                writer,
                poster, 
                imdb_rating, 
                imdb_votes, 
                imdb_id,
                type,
                saturation,
                brightness,
                entropy, 
                sharpness, 
                contrast,
                colorfulness,
                hex_0,
                hex_1,
                hex_2,
                hex_3,
                hex_4
                ):
        self.title = title
        self.year = year
        self.rated = rated
        self.released = released
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.writer = writer
        self.poster = poster
        self.imdb_rating = imdb_rating
        self.imdb_votes = imdb_votes
        self.imdb_id = imdb_id
        self.type = type
        self.saturation = saturation
        self.brightness = brightness
        self.entropy = entropy
        self.sharpness = sharpness
        self.contrast = contrast
        self.colorfulness = colorfulness
        self.hex_0 = hex_0
        self.hex_1 = hex_1
        self.hex_2 = hex_2
        self.hex_3 = hex_3 
        self.hex_4 = hex_4

    def __repr__(self):
        return f'Movie: {self.imdb_id}'

def format_movie(movie):
    return {
        'title': movie.title, 
        'year': movie.year, 
        'rated': movie.rated, 
        'released': movie.released, 
        'runtime': movie.runtime, 
        'genre': movie.genre, 
        'director': movie.director, 
        'writer': movie.writer,
        'poster': movie.poster, 
        'imdb_rating': movie.imdb_rating, 
        'imdb_votes': movie.imdb_votes, 
        'imdb_id': movie.imdb_id,
        'type': movie.type,
        'saturation': movie.saturation,
        'brightness': movie.brightness,
        'entropy': movie.entropy, 
        'sharpness': movie.sharpness, 
        'contrast': movie.contrast,
        'colorfulness': movie.colorfulness,
        'hex_0': movie.hex_0,
        'hex_1': movie.hex_1,
        'hex_2': movie.hex_2,
        'hex_3': movie.hex_3,
        'hex_4': movie.hex_4
    }

def format_poster(movie):
    return {
        'title': movie.title,
        'poster': movie.poster,
        'imdb_id': movie.imdb_id
    }

def format_features(movie):
    return {
        'saturation': movie.saturation,
        'brightness': movie.brightness,
        'entropy': movie.entropy, 
        'sharpness': movie.sharpness, 
        'contrast': movie.contrast,
        'colorfulness': movie.colorfulness,
        'hex_0': movie.hex_0,
        'hex_1': movie.hex_1,
        'hex_2': movie.hex_2,
        'hex_3': movie.hex_3,
        'hex_4': movie.hex_4
    }

@app.route('/')
def hello():
    return ('sup')

''' 
@app.route('/events', methods = ['GET'])
def get_events():
    events = Event.query.order_by(Event.created_at.asc()).all()
    event_list = [format_event(event) for event in events]
    return {
        'events': event_list
    }

@app.route('/events/<id>', methods = ['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).first()
    formated_event = format_event(event)
    return {
        'event': formated_event
        }
'''

@app.route('/movies', methods = ['GET'])
def get_movies():
    movies = Movie.query.order_by(Movie.year.desc()).all()
    movie_list = [format_movie(movie) for movie in movies]
    return {
        'Movies': movie_list
    }

@app.route('/movie/<id>', methods = ['GET'])
def get_movie_id(id):
    movie = Movie.query.filter_by(imdb_id=id).first()
    formated_movie = format_movie(movie)
    return {
        'Movie': formated_movie
        }

@app.route('/movie/search/<term>', methods = ['GET'])
def get_movies_search(term):
    movies = Movie.query.filter(Movie.title.ilike(f'%{term}%')).all()
    movie_list = [format_movie(movie) for movie in movies]
    return {
        'Movies': movie_list
    }

@app.route('/movie/poster/<id>', methods = ['GET'])
def get_movie_poster(id):
    movie = Movie.query.filter_by(imdb_id=id).first()
    formated_movie = format_poster(movie)
    return {
        'Poster': formated_movie
        }


@app.route('/features/l=<link>/n=<name>', methods=['GET'])
def get_features(link, name):
    location = str(f'./posters/{name}.jpg')
    get_content(location, str(link))
    return get_image_features(location, 100)

if __name__ == '__main__':
    app.run()
