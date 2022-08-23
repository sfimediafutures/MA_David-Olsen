from asyncio.log import logger
import cv2
import numpy as np
from sklearn.cluster import KMeans
from features import trim
import logging 
from collections import Counter
# All colors from all pixels in all keyframes are flattened
# and clustered. The top 10 centroids are picked as features
def get_all_colors(keyframes):   
    pal = []
    column_names = [f'color_channel_{i}' for i in range(10*3)]
    for img in keyframes:
        image = cv2.imread(img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        try: 
            thold = (image>20)*image
            image = trim(thold)
        except Exception as e:
            logging.error(e)
            image = image
        image = image[::20, ::20]

        image = image.reshape((image.shape[0] * image.shape[1], 3))

        for tup in image:
            pal.append(tup)
            
    pal_np = np.array(pal)[np.newaxis, :, :]
    sqz = pal_np.squeeze()

    clt = KMeans(n_clusters = 10)
    clt.fit(sqz)

    # Sorts colors from least to most dominant
    count = dict(Counter(clt.labels_))
    count = sorted(count.items(), key=lambda x:x[1])
    sortdict = dict(count)
    position = list(sortdict.keys())
    centers = clt.cluster_centers_ #.flatten().tolist()
    cols = centers[position].flatten().tolist()
    return dict(zip(column_names, cols))
