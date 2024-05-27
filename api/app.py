from flask import Flask, request, jsonify
import os
import numpy as np
from image_processing import predict_image_class
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app, support_credentials=True)
COORDINATES_FILE_PATH = os.path.join('exports', 'coordinates.txt')



# API endpoint to process image and extract coordinates
@app.route('/process-image', methods=['POST'])
@cross_origin(origin='*')
def process_image():
    if 'image' not in request.files:
        print("no image")
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_path = './uploads/' + image_file.filename
    image_file.save(image_path)

    # Predict class of the image
    class_labels_mapping = {0: 'Rose', 1: 'Common-dandelion', 2: 'Firethorn', 3: 'Sunflower', 4: 'Corn-poppy'}
    predicted_class = predict_image_class(image_path)
    predicted_class_label = class_labels_mapping[np.argmax(predicted_class)]

    response_data = {'plant_name': predicted_class_label}
    return jsonify(response_data),200


# API endpoint to save the entered coordinates with location information
@app.route('/save-coordinates', methods=['POST'])
@cross_origin(origin='*')
def save_coordinates():
    data = request.json
    coordinates = data.get('coordinates')

    if not coordinates or not isinstance(coordinates, list):
        return jsonify({'error': 'Invalid coordinates data'}), 400

    coordinates_text = ""
    for coord in coordinates:
        latitude = coord.get('latitude')
        longitude = coord.get('longitude')
        location_name = coord.get('location_name')
        if latitude is None or longitude is None or location_name is None:
            return jsonify({'error': 'Latitude, longitude, and location name are required for all coordinates'}), 400
        coordinates_text += f"Latitude: {latitude}\nLongitude: {longitude}\nLocation Name: {location_name}\n"

    try:
        with open(COORDINATES_FILE_PATH, 'a') as file:
            file.write(coordinates_text)
        return jsonify({'message': 'Coordinates and location name saved successfully', 'filePath': COORDINATES_FILE_PATH}), 200
    except Exception as e:
        return jsonify({'error': f'Error saving coordinates to file: {str(e)}'}), 500

    # Extract coordinates if the predicted class is "firethorn"
    # if predicted_class_label == 'firethorn':
    #     print("cords in api")
    #     coordinates = extract_coordinates(image_path)
    #     print("cords", coordinates)
    #     if coordinates:
    #         return jsonify({'coordinates': coordinates}), 200
    #     else:
    #         return jsonify({'error': 'No GPS data found in image'}), 400
    # else:
    #     return jsonify({'error': 'Image does not belong to firethorn class'}), 400

    # API endpoint to fetch saved coordinates

if __name__ == '__main__':
    app.run(debug=True, port=7541)