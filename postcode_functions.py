"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    try:
        with open(CACHE_FILE, "r", encoding="utf=8") as cache:
            return json.load(cache)
    except Exception:
        return {}


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, "w", encoding="utf=8") as file:
        json.dump(cache, file, indent=4)


def validate_postcode(postcode: str) -> bool:
    """Function which will send a request to the postcode 
    API and validate if it is a valid postcode"""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    url_base = "https://api.postcodes.io/postcodes/"
    URL = f"{url_base}{postcode}/validate"
    response = req.get(URL, timeout=5)
    if response.status_code != 200:
        if response.status_code == 500:
            raise req.RequestException("Unable to access API.")
        return False
    postcode_data = response.json()
    if postcode_data["result"] == False:
        return False
    return True


def get_postcode_for_location(lat: float, long: float) -> str:
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")
    url_base = "https://api.postcodes.io/postcodes?"
    URL = f"{url_base}lon={long}&lat={lat}"
    response = req.get(URL, timeout=5)
    if response.status_code != 200:
        if response.status_code == 500:
            raise req.RequestException("Unable to access API.")
        return False
    long_lat_data = response.json()
    if long_lat_data["result"] == None:
        raise ValueError("No relevant postcode found.")
    postcode = long_lat_data["result"][0]["postcode"]
    return postcode


def get_postcode_completions(postcode_start: str) -> list[str]:
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")
    url_base = "https://api.postcodes.io/postcodes/"
    URL = f"{url_base}{postcode_start}/autocomplete"
    response = req.get(URL, timeout=5)
    if response.status_code != 200:
        if response.status_code == 500:
            raise req.RequestException("Unable to access API.")
        return False
    postcode_completions = response.json()
    if postcode_completions["result"] == None:
        raise ValueError("No relevant postcode found.")
    return postcode_completions["result"]


def get_postcodes_details(postcodes: list[str]) -> list[dict]:
    if not isinstance(postcodes, list) or not all(isinstance(p, str) for p in postcodes):
        raise TypeError("Function expects a list of strings.")
    url_base = "https://api.postcodes.io/postcodes/"
    result = []
    for postcode in postcodes:
        postcode_f = postcode.replace(" ", "")
        URL = f"{url_base}{postcode_f}"
        response = req.get(URL, timeout=5)
        if response.status_code != 200:
            if response.status_code == 500:
                raise req.RequestException("Unable to access API.")
            return False
        postcode_data = response.json()
        # if postcode_data["result"] == None:
        #     raise ValueError("No relevant postcode found.")
        result.append[postcode_data["result"]]
    return result
