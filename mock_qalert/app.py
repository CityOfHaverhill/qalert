from datetime import datetime

from . import schemas

from flask import Flask, request, jsonify
import requests


QALERT_TEST_DATA_URL = "https://qalert-data.s3.us-east-2.amazonaws.com/requests_get.json"


app = Flask(__name__)


@app.route('/api/requests/get')
def requests_get_handler():
    params = schemas.GetRequestsSchema().load(request.values)
    sort = params.get('sort', None)
    count = params.get('count', None)
    create_date_min = params.get('create_date_min', None)

    qalert_requests = pull_qalert_test_data()

    if create_date_min:
        qalert_requests = list(filter(
            lambda qalert_request: datetime.strptime(qalert_request['createDate'], r"%m/%d/%Y %I:%M %p") > create_date_min,
            qalert_requests
        ))

    if sort:
        qalert_requests = sorted(
            qalert_requests,
            key=lambda qalert_request: datetime.strptime(qalert_request['createDate'], "%m/%d/%Y %I:%M %p")
        )

    if count and count != -1:
        qalert_requests = qalert_requests[:count]

    return jsonify(qalert_requests), 200


def pull_qalert_test_data():
    response = requests.get(url=QALERT_TEST_DATA_URL)
    qalert_data = response.json()
    return qalert_data
