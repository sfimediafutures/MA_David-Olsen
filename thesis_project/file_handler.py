import os
import pandas as pd 
import json
import requests
from pathlib import Path
#from i_frame import * 
from requests.structures import CaseInsensitiveDict
from pathlib import Path

import logging
import config

class ImageHandler(object):
    

    def __init__(self, config):
        self.config = config
    def get_poster(self, asset_id):  # sourcery skip: use-fstring-for-formatting

        ## render filename for local storage
        filename = "{}/{}.jpg".format(self.config.DATA_DIR, asset_id)
        logging.debug(filename)
        
        ## render url to asset API
        ## TODO: implement for series (shows, or categories)
        asset_url = "{}/assets/{}".format(self.config.URL_SUMO_API, asset_id)
        logging.debug(asset_url)
        
        ## get image pack id
        image_uri = get_image_uri(
            asset_url,
            self.config.IMAGE_PACK_ID_KEY,
            self.config.URL_IMAGE_API,
            self.config.IMAGE_STYLE_POSTER
            ## TODO: poster for movies, list for series
        )

        if image_uri is None:
            return None
        
        #logging.info(image_uri)
        
        ## store image locally
        get_content(filename, image_uri)

        return filename

class VideoHandler(object):
    
    def __init__(self, config):
        self.config = config

    def get_video(self, asset_id):  # sourcery skip: use-fstring-for-formatting
        
        ## render filename for local storage
        ## Video dir må være en submappe så den ikke leser av posters 
        filename = "{}/videofiles/{}/{}.mp4".format(self.config.DATA_DIR, asset_id, asset_id)
        logging.debug(filename)

        f = Path(filename)
        if f.is_file():
            logging.debug("file found", extra = {"file found": filename, "asset id": asset_id})
            return filename

        d = os.path.dirname(filename)
        if not os.path.exists(d):
            os.makedirs(d)
            
        ## render url to asset API
        asset_url = "{}{}/videoFiles".format(self.config.URL_TRAILER_API, asset_id)
        
        #logging.debug(asset_url)
        #print(asset_url)
        
        ## get image pack id
        trailer_uri = get_trailer_uri(
            asset_url,
            self.config.TRAILER_AUTH_TOKEN,
            self.config.TRAILER_BITRATE
        )

        if trailer_uri is None:
            return None
        
        #logging.info(trailer_uri)
        
        ## store image locally
        get_content(filename, trailer_uri)
        return filename

# Makes a list of unique assets from a series of assets
def get_assets(series):
    unique_list = []
    for x in series:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

# Get a specific title based on the movie title 
def get_asset(title: str, df, asset_col, title_col):
    return df[asset_col].loc[df[title_col] == title] 

# Gets url that is used to retrieve JSON object containing uri's 
def get_image_url(asset_id: str, url: str):
    return url+asset_id

def get_image_uri(url:str, image_pack_id, api, style):
    r = requests.get(url)
    if r.status_code != 200:
        logging.error("request failed for asset ({})".format(url))
        return None
    
    js = r.json()
    metadata = js['metadata']

    for dictionary in metadata:
        if (dictionary['name'] == image_pack_id):
            image_id = dictionary['value']

    return api+image_id+style

def get_trailer_uri(url:str, auth: str, rate):
    headers = CaseInsensitiveDict()
    r = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": "{}".format(auth)
        }
    )
    
    if r.status_code == 403:
        logging.error("request failed {}".format(r.status_code))
        logging.error("request failed {}".format(url))
        return None

    if r.status_code != 200:
        logging.error("request failed {}".format(r.status_code))
        logging.error("request failed {}".format(url))
        r.raise_for_status()

                      
    js = r.json()

    d = { str(x['bitrate']): x['uri'] for x in js }

    if str(rate) in d:
        logging.info("using videofile with bitrate {}".format(rate))
        return d[str(rate)]
        
    logging.warn("requested bitrate not found. using videofile with bitrate {}".format(js[0]['bitrate']))
    return js[0]['uri']
        

    

# Uses request library to download videofiles 
def get_content(filename, uri):
    r = requests.get(uri)
    if r.status_code != 200:
        logging.error("request failed", extra = uri)
        return None

    #print(r.status_code)
    #print(filename)
       
    f = open(filename, 'wb')
    for chunk in r.iter_content(chunk_size=255):
        if chunk:
            f.write(chunk)
    f.close

''' 
# Downloads all trailers in a batch
def batch_downloads(df, url: str, image_pack_id, image_api, poster_style, to_dir):
    #asset_ids = df[df['svod'] == True]
    asset_ids = get_assets(df['assetId'])

    out = []
     
    for asset_id in asset_ids:
        
        try: 
            #filename = df['assetId'][df['promoAssetId'] == asset_id]
            filename = "{}/{}.jpg".format(to_dir, asset_id)
            logging.info(filename)
            
            #filename = filename.iloc[0]
            compl_url = get_url(str(asset_id), url)
            logging.info(compl_url)
            
            #print(compl_url)
            uri = get_image_uri(compl_url, image_pack_id, image_api, poster_style)
            logging.info(uri)
            
            #logging.debug('URI gathred')
            get_image(filename, uri)
            logging.info(filename)

            out.append((asset_id, filename))
            print(out)
        except Exception:
            pass

    print(out)
    return out
'''    

if __name__ == "__main__":
    pass
    #env_var = load_dotenv('.env')
    #movie_path = os.getenv('TRAILERS')
    #movie_assets = os.getenv('MOVIE_ASSETS')
    #df = pd.read_csv(movie_assets)
    #url = os.getenv('IMAGE_URL')

    #print(get_image_uri('https://sumo.tv2.no/rest/assets/1557595'))
    #get_image('poster', get_image_uri('https://sumo.tv2.no/rest/assets/1557595'))
    #batch_downloads(df, url)
