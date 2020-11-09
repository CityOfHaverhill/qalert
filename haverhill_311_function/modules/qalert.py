"""The QAlert module is a wrapper client around the QAlert API."""
from . import settings

import requests

URL = settings.URL
API_KEY = settings.API_KEY
TEST_URL = settings.TEST_URL


def pull():
    """
    Makes a GET request to fetch 311 Data from QAlert API and returns the data.
    """
    data = []
    try:
        url = URL + "?key=" + API_KEY
        payload = {}
        headers = {}
        response = requests.request(
            "GET", url, headers=headers, data=payload
        )
        data = response.json()
        return data
    except Exception as exc:
        print(f"Network error: {exc}.")


def pull_data_test():
    """
    Makes an API call to sample test data of 311 requests from S3 bucket.
    """
    data = []
    try:
        payload = {}
        headers = {}
        response = requests.request(
            "GET", TEST_URL, headers=headers, data=payload)
        data = response.json()
        return data

    except Exception as e:
        print(e)
