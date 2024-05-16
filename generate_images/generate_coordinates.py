import requests
import csv


API_KEY = "Av9sOT2uny6SRjhcM7DPyN8aism5nZXIQyP715Yumlhy8Z6d8ElcVOSlnVVFiCVD"

def generate_coordinates(start_lat, start_lng, end_lat, end_lng, num_points):
    route_api_url = "http://dev.virtualearth.net/REST/v1/Routes/Driving"

    params = {
        "wayPoint.1": f"{start_lat},{start_lng}",
        "wayPoint.2": f"{end_lat},{end_lng}",
        "key": API_KEY,
        "optimize": "time",
        "routeAttributes": "routePath",
        "output": "json",
    }

    response = requests.get(route_api_url, params=params)
    data = response.json()

    coordinates = []
    if 'resourceSets' in data and len(data['resourceSets']) > 0 \
            and 'resources' in data['resourceSets'][0] and len(data['resourceSets'][0]['resources']) > 0 \
            and 'routePath' in data['resourceSets'][0]['resources'][0]:
        route_path = data['resourceSets'][0]['resources'][0]['routePath']['line']['coordinates']
        step = len(route_path) // (num_points - 1)
        for i in range(0, len(route_path), step):
            coordinates.append(route_path[i])

    return coordinates

def write_coordinates_to_csv(coordinates, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Latitude', 'Longitude'])
        for coord in coordinates:
            writer.writerow(coord)

# Example usage
start_lat, start_lng = 40.7128, -74.0060  
end_lat, end_lng = 34.0522, -118.2437  
num_points = 100
output_filename = "coordinates.csv"

coordinates = generate_coordinates(start_lat, start_lng, end_lat, end_lng, num_points)
write_coordinates_to_csv(coordinates, output_filename)
print(f"Coordinates saved to {output_filename}")
