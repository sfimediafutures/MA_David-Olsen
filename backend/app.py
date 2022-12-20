from math import nan
from unittest import result
import flask
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
# from features import get_content, get_image_features
import datetime

class JSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return flask.json.JSONEncoder.default(self, o)

app = flask.Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.json_encoder = JSONEncoder
client = MongoClient('mongodb://root:example@localhost:27017/')
movies = client.movies.posters_sim

@app.route("/api/", methods = ['GET'])
def home_page():
    all_movies = movies.find().limit(10)
    return flask.jsonify(list(all_movies))

@app.route("/api/movie/<movietype>", methods = ['GET'])
def get_movies(movietype):

    if (movietype == 'popular'):
        all_movies = movies.find({'imdbVotes':{'$ne': nan}}).sort('imdbVotes', -1).limit(20)
    elif (movietype == 'top_rated'):
        all_movies = movies.find({'imdbVotes':{'$gt': 1000}}).sort('imdbRating', -1).limit(20)
    elif (movietype[:2] == 'tt'):
        all_movies = movies.find({'imdbID': {'$regex':str(movietype)}})
    else:
        all_movies = movies.aggregate([{'$sample': {'size': 20}}])
    return flask.jsonify(list(all_movies))

@app.route("/api/genre/<genre>", methods = ['GET'])
def get_genre(genre):
    result = movies.find({'Genre': {'$regex':str(genre)}})
    return flask.jsonify(list(result))

@app.route("/api/search/movie/<film>", methods = ['GET'])
def get_search(film):
    result = movies.find({'Title':{'$regex': str(film)}}).limit(20)
    return flask.jsonify(list(result))

@app.route("/api/movie/<id>/credits", methods = ['GET'])
def get_credits(id):
    result = movies.find({'imdbID':{'$regex': str(id)}})
    return flask.jsonify(list(result))

# @app.route('/upload/<path:url>', methods=['GET'])
# def get_features(url):
#     location = 'tmp/'
#     get_content(location, str(url))
#     #i += 1
#     return get_image_features(location, 100)
    
@app.route("/api/similar/<id>", methods = ['GET'])
def get_similar(id):
    result = movies.find({'imdbID':{'$regex': str(id)}}, {'Similar':1})
    return flask.jsonify(list(result))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
