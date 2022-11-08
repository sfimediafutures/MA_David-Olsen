from pymongo import MongoClient
import json
from pprint import pprint
from dotenv import load_dotenv
from tqdm import tqdm
import requests
import os
client = MongoClient('mongodb://root:example@localhost:27017/')
backdrops = client.movies.backdrops
movies = client.movies.posters

load_dotenv()
TMDB = os.getenv('TMDB')

def get_backdrop(imdbid):
    try: 
        var = requests.get(f'https://api.themoviedb.org/3/find/{imdbid}?api_key={TMDB}&language=en-US&external_source=imdb_id')
        return var.json()['movie_results'][0]
    except Exception as e:
        return None
query = movies.find({'imdbVotes':{'$gt': 1000}}).sort('imdbRating', -1).limit(20)
query_all = movies.find()
# Popular
for x in tqdm(query_all):
    if not (backdrops.count_documents({'imdbID':x['imdbID']})):
        tmdbdata = get_backdrop(x['imdbID'])
        if tmdbdata:
            data = {
                'imdbID':x['imdbID'],
                'backdrop':tmdbdata['backdrop_path'],
                'overview':tmdbdata['overview'],
                'tmdbid':tmdbdata['id']
                }
            backdrops.find_one_and_update(data,
                                    {"$set": {"data": data}},
                                    upsert=True)
        else: pass
    else: pass