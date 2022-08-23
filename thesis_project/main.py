from keyframes import KeyframeProcessor
from image_handler import ImageHandler
from file_handler import VideoHandler

from import_asset_metadata import MetadataImporter
from kafka_producer import KafkaProducer
from kafka_consumer import KafkaConsumer
from poster_processor import process_poster
from trailer_processor import process_trailer

from pathlib import Path

import pandas as pd
import config
import logging
import glob

if __name__ == "__main__":
    config = config.Config.fromdict(config.defaultEnvVars)

    logger = logging.getLogger()
    logger.setLevel(level=config.LOGLEVEL)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('kafka').setLevel(logging.WARNING)
    logging.getLogger('elasticsearch').setLevel(logging.WARNING)

    logging.info("Importing item metadata")
    kafka_consumer = KafkaConsumer(config)
    asset_ids = kafka_consumer.read() 

    img_handler = ImageHandler(config)
    vid_handler = VideoHandler(config)
    keyframe_proc = KeyframeProcessor(config)
    kafka_producer = KafkaProducer(config)

    blacklist = []
    
    # movie posters
    for asset in asset_ids:
        logging.info("processing {}".format(asset))
        
        if not 'assetId' in asset:
            continue

        if asset['assetId'] in blacklist:
            logging.warn("skipping blacklisted asset ID {}".format(asset['assetId']))
            continue

        ## poster processing
        image_features = process_poster(asset, img_handler)

        if not image_features is None:
            kafka_producer.write(asset['assetId'], image_features, config.POSTER_MODEL_ID)

        if not 'promoAssetId' in asset:
            continue
            
        ## video processing
        video_features = process_trailer(asset, config, vid_handler, keyframe_proc)
        if not video_features is None:
            kafka_producer.write(asset['assetId'], video_features, config.TRAILER_MODEL_ID)
            kafka_producer.producer.flush()
        
    kafka_producer.producer.close()
    kafka_consumer.consumer.close()
        

    
