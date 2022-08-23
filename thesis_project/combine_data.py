import numpy as np
import statistics as stat
from features import *


# Gets the distance between 2 rows in a list
def mindistance(arr, N):
    return [arr[i] - arr[i-1] for i in range(1, N)]

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


def scene_matrix(d):
    N = len(d['scene_timestamp'])
    shot_length = mindistance(d['scene_timestamp'], N)
    shot_length = sorted(shot_length)
    
    try:
        average_shot_time = average(shot_length)
        median_shot_time = stat.median(shot_length)
        stdev_shot_time = stat.stdev(shot_length)
        shots_per_second = d['scene_nr'][N-1] / d['scene_timestamp'][N-1]
        
    except Exception as e:
        logging.debug(e)
        average_shot_time = 0
        median_shot_time = 0
        stdev_shot_time = 0
        shots_per_second = 0

    new_row = {
        'shots_per_second': shots_per_second, 
        'median_shot_time': median_shot_time, 
        'average_shot_time': average_shot_time,
        'stdev_shot_time': stdev_shot_time
    }

    return new_row

# New dataframe condensing each movie into a single row 
def movie_matrix(d):
    avg_brightness = average(d['brightness'])
    avg_saturation = average(d['saturation'])
    avg_entropy = average(d['entropy'])
    #avg_sharpness = average(d['sharpness'])
    avg_contrast = average(d['contrast'])
    avg_colorfulness = average(d['colorfulness'])

    stdev_brightness = stat.stdev((d['brightness']))
    stdev_saturation = stat.stdev((d['saturation']))
    stdev_entropy = stat.stdev((d['entropy']))
    #stdev_sharpness = stat.stdev((d['sharpness']))
    stdev_contrast = stat.stdev((d['contrast']))
    stdev_colorfulness = stat.stdev((d['colorfulness']))

    median_brightness = stat.median((d['brightness']))
    median_saturation = stat.median((d['saturation']))
    median_entropy = stat.median((d['entropy']))
    #median_sharpness = stat.median((d['sharpness']))
    median_contrast = stat.median((d['contrast']))
    median_colorfulness = stat.median((d['colorfulness']))

    matrix_dict = {
        'avg_brightness': avg_brightness,
        'avg_saturation': avg_saturation,
        'avg_entropy': avg_entropy,
        #'avg_sharpness': avg_sharpness,
        'avg_contrast': avg_contrast,
        'avg_colorfulness': avg_colorfulness,
        'stdev_brightness': stdev_brightness,
        'stdev_saturation': stdev_saturation,
        'stdev_entropy': stdev_entropy,
        #'stdev_sharpness': stdev_sharpness,
        'stdev_contrast': stdev_contrast,
        'stdev_colorfulness': stdev_colorfulness,
        'median_brightness': median_brightness,
        'median_saturation': median_saturation,
        'median_entropy': median_entropy,
        #'median_sharpness': median_sharpness,
        'median_contrast': median_contrast,
        'median_colorfulness': median_colorfulness,
    }

    return matrix_dict

# Polynomial regression on the features related to the mobies
def polynomial_regression(d):

    frame_nr = d['frame_nr']
    saturation = d['saturation']
    brightness = d['brightness']
    entropy = d['entropy']
    #sharpness = d['sharpness']
    contrast = d['contrast']
    colorfulness = d['colorfulness']

    saturation_model_1st = np.poly1d(np.polyfit(frame_nr, saturation, 1))
    brightness_model_1st = np.poly1d(np.polyfit(frame_nr, brightness, 1))
    entropy_model_1st = np.poly1d(np.polyfit(frame_nr, entropy, 1))
    #sharpness_model_1st = str(np.poly1d(np.polyfit(frame_nr, sharpness, 1)))
    contrast_model_1st = np.poly1d(np.polyfit(frame_nr, contrast, 1))
    colorfulness_model_1st = np.poly1d(np.polyfit(frame_nr, colorfulness, 1))

    saturation_model_2nd = np.poly1d(np.polyfit(frame_nr, saturation, 2))
    brightness_model_2nd = np.poly1d(np.polyfit(frame_nr, brightness, 2))
    entropy_model_2nd = np.poly1d(np.polyfit(frame_nr, entropy, 2))
    #sharpness_model_2nd = str(np.poly1d(np.polyfit(frame_nr, sharpness, 2)))
    contrast_model_2nd = np.poly1d(np.polyfit(frame_nr, contrast, 2))
    colorfulness_model_2nd = np.poly1d(np.polyfit(frame_nr, colorfulness, 2))

    polynomial_dict = {
        'saturation_model_1st': saturation_model_1st.c[0], 
        'brightness_model_1st': brightness_model_1st.c[0],
        'entropy_model_1st': entropy_model_1st.c[0],
        #'sharpness_model_1st': sharpness_model_1st.c[0],
        'contrast_model_1st': contrast_model_1st.c[0],
        'colorfulness_model_1st': colorfulness_model_1st.c[0],

        'saturation_model_2nd_c1': saturation_model_2nd.c[0],
        'saturation_model_2nd_c2': saturation_model_2nd.c[1],
        'brightness_model_2nd_c1': brightness_model_2nd.c[0],
        'brightness_model_2nd_c2': brightness_model_2nd.c[1],
        'entropy_model_2nd_c1': entropy_model_2nd.c[0],
        'entropy_model_2nd_c2': entropy_model_2nd.c[1],
        #'sharpness_model_2nd_c1': sharpness_model_2nd.c[0],
        #'sharpness_model_2nd_c2': sharpness_model_2nd.c[1],
        'contrast_model_2nd_c1': contrast_model_2nd.c[0],
        'contrast_model_2nd_c2': contrast_model_2nd.c[1],
        'colorfulness_model_2nd_c1': colorfulness_model_2nd[0],
        'colorfulness_model_2nd_c2': colorfulness_model_2nd[1],
    }

    return polynomial_dict

# Combines shot data with visualfeatures
def combine_data(features, scene_features, color_dict):

    poly = polynomial_regression(features)
    matrix = movie_matrix(features)

    ## TODO: no-poly ??
    out = poly | matrix | scene_features | color_dict
    
    return out
