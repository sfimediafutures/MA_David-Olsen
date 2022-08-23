import logging
from file_handler import *
from combine_data import *
from keyframes import *
from trailer_colors import get_all_colors
import shutil


def process_trailer(asset, config, vid_handler, keyframe_proc):

    trailer_asset_id = asset['promoAssetId'] 
    movie_asset_id = asset['assetId']
        
    logging.debug(f'processing trailer {trailer_asset_id}')

    # download video file
    video_filename = vid_handler.get_video(trailer_asset_id)
    if video_filename is None:
        logging.warn(f"skipping asset ID {movie_asset_id}; trailer ID {trailer_asset_id}")
        return None
    
    # extract keyframes
    keyframes = keyframe_proc.get_key_frames(video_filename, trailer_asset_id, int(config.TRAILER_KEYFRAMES))
    if keyframes is None:
        logging.warn(f"skipping asset ID {movie_asset_id}; trailer ID {trailer_asset_id}")
        return None

    # calculate visual features as dictonary
    features = get_video_features(keyframes, trailer_asset_id, 'low')
    #print("-- features --")
    #print(features)

    try:
        colors = get_all_colors(keyframes)
    except IndexError as e:
        logging.error(e)
        logging.error("could not get colors for asset {} / {}".format(trailer_asset_id, movie_asset_id))
        return None        

    #print("-- colors --")
    #print(colors)

    # find scenes
    scenes = find_scenes(video_filename)
    #print("-- scenes --")
    #print(scenes)

    # stats on scences / clipping
    scene_features = scene_matrix(scenes)
    #print("-- scene-features --")
    #print(scene_features)

    # reduce feature matrix to vector
    # TODO: include scene-features
    try:
        results = combine_data(features, scene_features, colors)
    except IndexError as e:
        logging.error(e)
        logging.error("could not combine data for asset {} / {}".format(trailer_asset_id, movie_asset_id))
        return None        
        
    #print(" -- final results --")
    #print(results)

    
    if len(keyframes) > 0:
        keyframe_dir = os.path.dirname(keyframes[0])
        logging.debug("removing keyframes in {}".format(keyframe_dir))
        [os.remove(x) for x in keyframes]
        os.rmdir(keyframe_dir)
        
        
    logging.debug("removing directory {}".format(os.path.dirname(video_filename)))
    #os.rmdir(os.path.dirname(video_filename))
    shutil.rmtree((os.path.dirname(video_filename)))
    
    return results
