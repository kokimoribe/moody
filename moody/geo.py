"""Helper functions to handle location context are defined here"""

import requests

from moody.config import GOOGLE_API_KEY


def google_places_from_coord(latitude, longitude):
    """
    Query places near given coordinates from Google Places API

    This can be done by using their web service via HTTP:
    https://developers.google.com/places/web-service/search

    Or can be done via Google Maps Python SDK:
    https://github.com/googlemaps/google-maps-services-python

    For this implementation, we'll be using their HTTP web service via the python `requests` module.
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    query_params = {
        "location": f"{latitude},{longitude}",
        "radius": "100",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=query_params)
    response.raise_for_status()

    # Example responses can be found in Google Places API documentation:
    # https://developers.google.com/places/web-service/search
    response_body = response.json()
    places = [
        {
            "place_id": result["place_id"],
            "name": result["name"],
            "types": result["types"],
            "latitude": result["geometry"]["location"]["lat"],
            "longitude": result["geometry"]["location"]["long"]
        }
        for result in response_body["results"]
    ]

    return places
