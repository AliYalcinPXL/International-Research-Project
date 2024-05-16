import json
import re
from typing import List, Optional

import requests
from pydantic import BaseModel
from requests.models import Response


class Panorama(BaseModel):
    pano_id: str
    lat: float
    lon: float
    heading: float
    pitch: Optional[float]
    roll: Optional[float]
    date: Optional[str]


def make_search_url(lat: float, lon: float) -> str:
    """
    Builds the URL to search for panoramas using Bing Maps API.
    """
    url = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/Panorama/{lat},{lon}/5?key=YOUR_BING_MAPS_API_KEY"
    return url


def search_request(lat: float, lon: float) -> Response:
    """
    Gets the response of the script on Bing Maps API that returns the
    closest panoramas (ids) to a given GPS coordinate.
    """
    url = make_search_url(lat, lon)
    return requests.get(url)


def extract_panoramas(data: dict) -> List[Panorama]:
    """
    Extracts panoramas from the response of Bing Maps API.
    """
    panoramas = []
    for resource in data["resourceSets"][0]["resources"]:
        panoramas.append(
            Panorama(
                pano_id=resource["name"],
                lat=resource["point"]["coordinates"][0],
                lon=resource["point"]["coordinates"][1],
                #heading=0,  # Bing Maps doesn't provide heading information directly
                pitch=None,
                roll=None,
                date=None,
            )
        )
    return panoramas


def search_panoramas(lat: float, lon: float) -> List[Panorama]:
    """
    Gets the closest panoramas to the GPS coordinates using Bing Maps API.
    """
    resp = search_request(lat, lon)
    if resp.status_code == 200:
        data = resp.json()
        pans = extract_panoramas(data)
        return pans
    else:
        print(f"Error: {resp.status_code} - {resp.text}")
        return []


