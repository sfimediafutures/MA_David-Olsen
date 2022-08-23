import os
import cv2
import numpy as np
from skimage.filters.rank import entropy
from skimage.morphology import disk
from sklearn.cluster import KMeans
import logging
from collections import Counter
#import pandas as pd



# Standard PySceneDetect imports:
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
# For caching detection metrics and saving/loading to a stats file
from scenedetect.stats_manager import StatsManager
# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector

# Averages a list
def average(l):
    return sum(l) / len(l)

# Makes a list of unique values from a list
def unique(list1):
    # Init null list
    unique_list = []

    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
            #print(x)
    return unique_list

# Calculates brightness by splitting HSV color space into 
# hue, saturation, and value. The value is synonymous with brightness.
def get_brightness(img):
    image = img.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #cv2.imshow('Image', hsv)
    _, _, v = cv2.split(hsv)
    sum = np.sum(v, dtype=np.float32)
    num_of_pixels = v.shape[0] * v.shape[1]
    return (sum * 100.0) / (num_of_pixels * 255.0)

# Calculates saturation by splitting HSV color space into 
# hue, saturation, and value. Saturation is extracted and represents
# saturation
def get_saturation(img):
    image = img.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #cv2.imshow('Image', hsv)
    _, s, _ = cv2.split(hsv)
    sum = np.sum(s, dtype = np.float32)
    num_of_pixels = s.shape[0] * s.shape[1]
    return (sum * 100.0) / (num_of_pixels * 255.0)

# Calculates entropy
def get_entropy(img):
    image = img.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    entropy_img = entropy(gray,disk(5))
    all_sum = np.sum(entropy_img, dtype = np.float32)
    num_of_pixels = entropy_img.shape[0] * entropy_img.shape[1]
    return all_sum / num_of_pixels

# Calculates image sharpness by the variance of the Laplacian
def get_sharpness(img):
    image = img.copy()
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(img2gray, cv2.CV_64F).var()

# Return contrast (RMS contrast)
def get_contrast(img):
    image = img.copy()
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return img_gray.std()

def get_colorfulness(img):
    image = img.copy()
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))
    # compute rg = R - G
    rg = np.absolute(R - G)
    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)
    # compute the mean and standard deviation of both `rg` and `yb`
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    # combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    # derive the "saturation" metric and return it
    return stdRoot + (0.3 * meanRoot)

def get_poster_colors(img):    
    pal = []
    column_names = [f'color_channel_{i}' for i in range(5*3)]
    image = img.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image[::10, ::10]

    image = image.reshape((image.shape[0] * image.shape[1], 3))

    for tup in image:
        #print(tup)
        pal.append(tup)
    #pal_np = np.array(pal)[np.newaxis, :, :]
    #sqz = pal.squeeze()

    clt = KMeans(n_clusters = 5)
    clt.fit(pal)
    count = dict(Counter(clt.labels_))
    count = sorted(count.items(), key=lambda x:x[1])
    sortdict = dict(count)
    position = list(sortdict.keys())
    centers = clt.cluster_centers_ #.flatten().tolist()
    cols = centers[position].flatten().tolist()

    return dict(zip(column_names, cols))

# Trims edges from images
def trim(frame):
    #crop top
    if not np.sum(frame[0]):
        return trim(frame[1:])
    #crop bottom
    elif not np.sum(frame[-1]):
        return trim(frame[:-2])
    #crop left
    elif not np.sum(frame[:,0]):
        return trim(frame[:,1:]) 
    #crop right
    elif not np.sum(frame[:,-1]):
        return trim(frame[:,:-2])    
    return frame

# Adds values for each picture to a list so they can be later averaged and 
# made into a dataframe. 
def get_video_features(keyframes, asset_id, downsampling: str):
    movie_dict = {}

    saturation_list = []
    brightness_list = []
    entropy_list = []
    #sharpness_list = []
    contrast_list = []
    colorfulness_list = []

    frame_list = []

    for frame in keyframes:
        try:
            img = cv2.imread(frame)

            if downsampling == 'low':
                img = img[::5,::5]
            elif downsampling == 'high':
                img = img[::10,::10]

            # Removes black borders from keyframes 
            # In case trailers with different aspect 
            # ratios are being used. 
            try: 
                thold = (img>20)*img
                img = trim(thold)
            except Exception as e:
                logging.debug(e)
                img = img

            frame_brightness = get_brightness(img)
            frame_saturation = get_saturation(img)
            frame_entropy = get_entropy(img)
            #frame_sharpness = get_sharpness(img)
            frame_contrast = get_contrast(img)
            frame_colorfulness = get_colorfulness(img)

            saturation_list.append(frame_saturation)
            brightness_list.append(frame_brightness)
            entropy_list.append(frame_entropy)
            #sharpness_list.append(frame_sharpness)
            contrast_list.append(frame_contrast)
            colorfulness_list.append(frame_colorfulness)

            ## remove .jpg from filename, cast to int
            ## TODO: might go terribly wrong
            frame_nr = int(os.path.basename(frame[:-4]))
            frame_list.append(frame_nr)
        except Exception as e:
            logging.debug(e)

    # Create movie dictionary
    movie_dict = {
        'saturation': saturation_list, # list with a value per frame
        'brightness': brightness_list, 
        'entropy': entropy_list, 
        #'sharpness': sharpness_list, 
        'contrast': contrast_list,
        'colorfulness': colorfulness_list,
        'frame_nr': frame_list,
        #'movie_id': asset_id
    }

    logging.info(f'Features successfully extracted for asset ID {asset_id}')
    return movie_dict


def get_image_features(filename, scale_percent):
    try:
        img = cv2.imread(filename)
        scale_percent = scale_percent # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        image_dict = {
            'saturation': get_saturation(img),
            'brightness': get_brightness(img),
            'entropy': get_entropy(img),
            'sharpness': get_sharpness(img),
            'contrast': get_contrast(img),
            'colorfulness': get_colorfulness(img),
        }

        # get_poster_colors returns a dictionary
        # therefore this is merged with the image_dict
        color_dict = get_poster_colors(img)
        image_dict = image_dict | color_dict
        #image_dict['dominant_color'] = [y for x in image_dict['dominant_color'] for y in x ]
        
    except Exception as e:
        logging.error(e)
        #logging.error(f'Error at image {image_folder[i][:-4]}')

    return image_dict

def find_scenes(video_path):
    
    video_manager = VideoManager([video_path])

    stats_manager = StatsManager()

    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)

    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector())

    scene_list = []
    #temp_df = pd.DataFrame(columns=['scene_nr', 'scene_timestamp', 'movie_id'])

    try:
        # Set downscale factor to improve processing speed.
        video_manager.set_downscale_factor(1)
        
        # Start video_manager.
        video_manager.start()
        
        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager)
        
        # Obtain list of detected scenes.
        # Each scene is a tuple of (start, end) FrameTimecodes.
        scene_list = scene_manager.get_scene_list()

        scene_nr = []
        scene_timestamp = []
        
        for i, scene in enumerate(scene_list):            
            scene_nr.append(i)
            scene_timestamp.append(scene[0].get_seconds())            
            
    finally:
        video_manager.release()

    data = {"scene_nr": scene_nr, "scene_timestamp": scene_timestamp}
    
    return data
