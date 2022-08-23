import logging
from features import get_image_features


def process_poster(asset, img_handler):

    asset_id = asset['assetId']
    logging.debug(f"processing {asset_id}")
    
    ## downloads poster image to disk
    image_filename = img_handler.get_poster(asset_id)

    if image_filename is None:
        return None

    ## fetch visual features of image
    image_features = get_image_features(image_filename, 35)

    return image_features
