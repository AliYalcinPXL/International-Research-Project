from flask import Flask, request, jsonify
import os
import numpy as np
from image_processing import predict_image_class, extract_coordinates
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app, support_credentials=True)


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
    class_labels_mapping = {0: 'rose', 1: 'common-dandelion', 2: 'firethorn', 3: 'sunflower', 4: 'corn-poppy'}
    predicted_class = predict_image_class(image_path)
    predicted_class_label = class_labels_mapping[np.argmax(predicted_class)]

    response_data = {'plant_name': predicted_class_label}
    return jsonify(response_data),200


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

if __name__ == '__main__':
    app.run(debug=True, port=7541)