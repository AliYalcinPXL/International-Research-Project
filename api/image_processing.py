import os
import exifread
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

# Load the trained model
classifier = load_model('classifier.keras')

# Function to predict class of an image
def predict_image_class(image_path):
    print("in perdiction")
    print(image_path)
    image = load_img(image_path, target_size=(64, 64))
    image_array = img_to_array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    prediction = classifier.predict(image_array)
    print("pred ", prediction)
    return prediction

# Function to extract coordinates from image metadata
# def extract_coordinates(image_path):
#     print("extracting cords")
#     with open(image_path, 'rb') as f:
#         tags = exifread.process_file(f)
#         print("tags: ", tags)
#         lat = tags.get('GPS GPSLatitude')
#         lon = tags.get('GPS GPSLongitude')
#         lat_ref = tags.get('GPS GPSLatitudeRef')
#         lon_ref = tags.get('GPS GPSLongitudeRef')
#         print("printing cord details\n")
#         print(lat, lon, lat_ref, lon_ref)

#         if lat and lon and lat_ref and lon_ref:
#             lat = [float(x.num) / float(x.den) for x in lat.values]
#             lon = [float(x.num) / float(x.den) for x in lon.values]
#             lat = lat[0] + lat[1] / 60 + lat[2] / 3600
#             lon = lon[0] + lon[1] / 60 + lon[2] / 3600
#             if lat_ref.values != 'N':
#                 lat = -lat
#             if lon_ref.values != 'E':
#                 lon = -lon
#             return lat, lon

#     return None
