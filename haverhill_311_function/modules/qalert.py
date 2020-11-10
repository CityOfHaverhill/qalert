"""The QAlert module is a wrapper client around the QAlert API."""
from . import settings

import requests


def pull():
    """
    Makes a GET request to fetch 311 Data from QAlert API and returns the data.
    """
    if settings.TEST:
        url = settings.QALERT_REQUEST_ENDPOINT_TEST
    else:
        url = settings.QALERT_REQUEST_ENDPOINT + "?key=" + settings.QALERT_API_KEY
    payload = {}
    headers = {}
    response = requests.get(url, headers=headers, data=payload)
    data = response.json()
    return data
