import os
from streetview import get_streetview
from generate_coordinates import generate_coordinates, write_coordinates_to_csv

# Constants
OUTPUT_FOLDER = "images"  # Folder to store the generated images
Bing_Maps_API_Key= 'Av9sOT2uny6SRjhcM7DPyN8aism5nZXIQyP715Yumlhy8Z6d8ElcVOSlnVVFiCVD'
#-28,480011, 28,796427
# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Generate coordinates
start_lat, start_lng = (-28.480011, 28.796427 ) 
end_lat, end_lng = (-28.506300, 28564395 ) 
num_points = 100
output_filename = "coordinates.csv"

generate_coordinates(start_lat, start_lng, end_lat, end_lng, num_points)
def read_coordinates_from_csv(csv_file):
    coordinates_list = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            latitude, longitude = map(float, row)
            coordinates_list.append((latitude, longitude))
    return coordinates_list

csv_file = 'coordinates.csv'
coordinates = read_coordinates_from_csv(csv_file)

# Retrieve panoramas for each coordinate
for i, (lat, lon) in enumerate(coordinates):
    pano_id = f"pano_{i}"
    image_filename = os.path.join(OUTPUT_FOLDER, f"{pano_id}.jpg")
    try:
        street_view_image = get_streetview(pano_id=pano_id, api_key=Bing_Maps_API_Key, width=640, height=640, fov=120, pitch=0)
        street_view_image.save(image_filename)
        print(f"Panorama {i+1}/{len(coordinates)} saved to {image_filename}")
    except Exception as e:
        print(f"Failed to retrieve panorama for coordinates {lat}, {lon}: {e}")
