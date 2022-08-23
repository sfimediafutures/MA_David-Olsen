import os 
import numpy as np
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
from pathlib import Path
import logging


# Custom disk writer class used to ommit 
# Filepath from keyframe filename
# Only the frame number is kept
class CustomDiskWriter(KeyFrameDiskWriter):

    def generate_output_filename(self, filepath, keyframe_number):
        """Generates the filename of output data file.

        :param filepath: path of the file
        :type filepath: str
        :param keyframe_number: keyframe number
        :type keyframe_number: int
        :return: name of the output file 
        :rtype: str
        """

        file_name_arr = []

        # append the keyframe number
        file_name_arr.append(str(keyframe_number))
        
        # Crashes if returning list instead of doing this
        # 
        filename = "".join(file_name_arr)
        
        return filename


# Main extraction function
# Takes in the complete path to the video file being sampled
class KeyframeProcessor(object):

    def __init__(self, config):
        self.config = config

    def get_key_frames(self, video_filename, asset_id, no_of_keyframes):
        
        video_dirname = os.path.dirname(video_filename)
        keyframe_dir = f"{video_dirname}/keyframes"

        if not os.path.exists(keyframe_dir):
                os.mkdir(keyframe_dir)
   

        # initialize diskwriter to save data at desired location
        diskwriter = CustomDiskWriter(location=keyframe_dir, file_ext=".jpg") 

        # initialize video module
        vd = Video()

        # extract keyframes and process data with diskwriter
        try:
            vd.extract_video_keyframes(
                no_of_frames=no_of_keyframes,  
                file_path=video_filename,
                writer=diskwriter
            )
        except ValueError as e:
            logging.error("could not fetch keyframes for {}".format(asset_id))
            logging.error(e)
            return []
        
        
        keyframes = []
        for num in range(no_of_keyframes):
            keyframe_file = Path(f"{keyframe_dir}/{num}.jpg")
            if keyframe_file.is_file():
                keyframes.append(f"{keyframe_dir}/{num}.jpg")

        if len(keyframes) == 0:
            logging.error("missing keyframes")
        else:
            logging.info("{} keyframes".format(len(keyframes)))

        return keyframes
