"""The QAlert module is a wrapper client around the QAlert API for pulling 311 request data."""

import os
import requests
import json
import settings

URL = settings.URL
API_KEY = settings.API_KEY
TEST_URL = settings.TEST_URL


def pull():
    data = []
    try:
        url = URL + "?key=" + API_KEY
        payload = {}
        headers = {}
        response = requests.request(
            "GET", url, headers=headers, data=payload
        )

    except:
        print("Network error.")

    try:
        data = response.json()
        return data

    except Exception as e:
        print(e)
        raise


def pull_data_test():
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
