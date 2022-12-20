# import os
# import cv2
# import numpy as np
# from skimage.filters.rank import entropy
# from skimage.morphology import disk
# from sklearn.cluster import KMeans
# import logging
# import requests
# from collections import Counter
# import pandas as pd

# # Averages a list
# def average(l):
#     return sum(l) / len(l)

# # Makes a list of unique values from a list
# def unique(list1):
#     # Init null list
#     unique_list = []

#     for x in list1:
#         if x not in unique_list:
#             unique_list.append(x)
#             #print(x)
#     return unique_list

# # Calculates brightness by splitting HSV color space into 
# # hue, saturation, and value. The value is synonymous with brightness.
# def get_brightness(img):
#     image = img.copy()
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     #cv2.imshow('Image', hsv)
#     _, _, v = cv2.split(hsv)
#     sum = np.sum(v, dtype=np.float32)
#     num_of_pixels = v.shape[0] * v.shape[1]
#     return (sum * 100.0) / (num_of_pixels * 255.0)

# # Calculates saturation by splitting HSV color space into 
# # hue, saturation, and value. Saturation is extracted and represents
# # saturation
# def get_saturation(img):
#     image = img.copy()
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     #cv2.imshow('Image', hsv)
#     _, s, _ = cv2.split(hsv)
#     sum = np.sum(s, dtype = np.float32)
#     num_of_pixels = s.shape[0] * s.shape[1]
#     return (sum * 100.0) / (num_of_pixels * 255.0)

# # Calculates entropy
# def get_entropy(img):
#     image = img.copy()
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     entropy_img = entropy(gray,disk(5))
#     all_sum = np.sum(entropy_img, dtype = np.float32)
#     num_of_pixels = entropy_img.shape[0] * entropy_img.shape[1]
#     return all_sum / num_of_pixels

# # Calculates image sharpness by the variance of the Laplacian
# def get_sharpness(img):
#     image = img.copy()
#     img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     return cv2.Laplacian(img2gray, cv2.CV_64F).var()

# # Return contrast (RMS contrast)
# def get_contrast(img):
#     image = img.copy()
#     img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     return img_gray.std()

# def get_colorfulness(img):
#     image = img.copy()
#     # split the image into its respective RGB components
#     (B, G, R) = cv2.split(image.astype("float"))
#     # compute rg = R - G
#     rg = np.absolute(R - G)
#     # compute yb = 0.5 * (R + G) - B
#     yb = np.absolute(0.5 * (R + G) - B)
#     # compute the mean and standard deviation of both `rg` and `yb`
#     (rbMean, rbStd) = (np.mean(rg), np.std(rg))
#     (ybMean, ybStd) = (np.mean(yb), np.std(yb))
#     # combine the mean and standard deviations
#     stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
#     meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
#     # derive the "saturation" metric and return it
#     return stdRoot + (0.3 * meanRoot)

# def get_image_colors(img):    
#     pal = []
#     column_names = [f'color_channel_{i}' for i in range(5*3)]
#     image = img.copy()
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image = image[::10, ::10]

#     image = image.reshape((image.shape[0] * image.shape[1], 3))

#     for tup in image:
#         #print(tup)
#         pal.append(tup)
#     #pal_np = np.array(pal)[np.newaxis, :, :]
#     #sqz = pal.squeeze()

#     clt = KMeans(n_clusters = 5)
#     clt.fit(pal)
#     count = dict(Counter(clt.labels_))
#     count = sorted(count.items(), key=lambda x:x[1])
#     sortdict = dict(count)
#     position = list(sortdict.keys())
#     centers = clt.cluster_centers_ #.flatten().tolist()
#     cols = centers[position].flatten().tolist()

#     return dict(zip(column_names, cols))

# # Trims edges from images
# def trim(frame):
#     #crop top
#     if not np.sum(frame[0]):
#         return trim(frame[1:])
#     #crop bottom
#     elif not np.sum(frame[-1]):
#         return trim(frame[:-2])
#     #crop left
#     elif not np.sum(frame[:,0]):
#         return trim(frame[:,1:]) 
#     #crop right
#     elif not np.sum(frame[:,-1]):
#         return trim(frame[:,:-2])    
#     return frame


# def get_image_features(filename, scale_percent):
#     image_dict = {}
#     try:
#         img = cv2.imread(filename)
#         scale_percent = scale_percent # percent of original size
#         width = int(img.shape[1] * scale_percent / 100)
#         height = int(img.shape[0] * scale_percent / 100)
#         dim = (width, height)
#         img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#         image_dict = {
#             'saturation': get_saturation(img),
#             'brightness': get_brightness(img),
#             'entropy': get_entropy(img),
#             'sharpness': get_sharpness(img),
#             'contrast': get_contrast(img),
#             'colorfulness': get_colorfulness(img),
#         }

#         # get_image_colors returns a dictionary
#         # therefore this is merged with the image_dict
#         rgb_color_dict = get_image_colors(img)

#         hex_color_dict = {
#             'hex_0': '#%02x%02x%02x' % (int(rgb_color_dict['color_channel_0']), int(rgb_color_dict['color_channel_1']), int(rgb_color_dict['color_channel_2'])),
#             'hex_1': '#%02x%02x%02x' % (int(rgb_color_dict['color_channel_3']), int(rgb_color_dict['color_channel_4']), int(rgb_color_dict['color_channel_5'])),
#             'hex_2': '#%02x%02x%02x' % (int(rgb_color_dict['color_channel_6']), int(rgb_color_dict['color_channel_7']), int(rgb_color_dict['color_channel_8'])),
#             'hex_3': '#%02x%02x%02x' % (int(rgb_color_dict['color_channel_9']), int(rgb_color_dict['color_channel_10']), int(rgb_color_dict['color_channel_11'])),
#             'hex_4': '#%02x%02x%02x' % (int(rgb_color_dict['color_channel_12']), int(rgb_color_dict['color_channel_13']), int(rgb_color_dict['color_channel_14']))
#         }

#         image_dict = image_dict | hex_color_dict
#         #image_dict['dominant_color'] = [y for x in image_dict['dominant_color'] for y in x ]
        
#     except Exception as e:
#         logging.error(e)
#         #logging.error(f'Error at image {image_folder[i][:-4]}')

#     return image_dict

# def get_content(filename, uri):
#     r = requests.get(uri)
#     if r.status_code != 200:
#         logging.error("request failed", extra = uri)
#         return None

#     #print(r.status_code)
#     #print(filename)
       
#     f = open(filename, 'wb')
#     for chunk in r.iter_content(chunk_size=255):
#         if chunk:
#             f.write(chunk)
#     f.close


# if __name__ == '__main__': 
#    feats = get_image_features('/Users/davidkvasnesolsen/Desktop/final/mongo-backend/dog.jpg', 100)
#    print(feats)
