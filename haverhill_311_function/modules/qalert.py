"""The QAlert module is a wrapper client around the QAlert API."""
from . import settings
from . import db

import requests


def pull():
    """
    Makes a GET request to fetch 311 Data from QAlert API and returns the data.
    """

    data = []
    if settings.TEST:
        url = settings.QALERT_REQUEST_ENDPOINT_TEST
    else:
        url = "{endpoint}?key={api_key}&count={count}".format(
            endpoint=settings.QALERT_REQUEST_ENDPOINT,
            api_key=settings.QALERT_API_KEY,
            count=-1
        )
        create_date_min = None
        with db.QAlertAuditDB() as audit_db:
            latest_request = audit_db.get_latest_request()

        if latest_request is not None:
            create_date_min = latest_request.create_date

        if create_date_min is not None:
            url += "&createDateMin=" + create_date_min
    payload = {}
    headers = {'User-Agent': 'Custom'}
    response = requests.request(
        "GET", url, headers=headers, data=payload
    )
    if type(response) == requests.models.Response:
        return response
    data = response.json()
    return data
