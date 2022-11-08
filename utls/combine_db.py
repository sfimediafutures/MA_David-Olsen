from pymongo import MongoClient
import json
from pprint import pprint
from dotenv import load_dotenv
from tqdm import tqdm

client = MongoClient('mongodb://root:example@localhost:27017/')
backdrops = client.movies.backdrops
movies = client.movies.posters

backdrops_entries = backdrops.find()

for entry in tqdm(backdrops_entries):
    data = {
        "backdrop": entry['backdrop'],
        "overview": entry['overview'],
        "tmdbid": entry['tmdbid'],
    }
    movies.find_one_and_update({"imdbID": entry['imdbID']}, 
                                 {"$set": data})