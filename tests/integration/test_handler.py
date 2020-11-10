import os

os.environ.update({
    "QALERT_REQUEST_ENDPOINT": "blah",
    "QALERT_API_KEY": "blah",
    "QALERT_REQUEST_ENDPOINT_TEST": "https://qalert-data.s3.us-east-2.amazonaws.com/requests_get.json",  # noqa: E501
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_USER": "docker",
    "DB_PASSWORD": "docker",
    "DB_DATABASE": "qalert_test",
    "TEST": "true"
})

from haverhill_311_function import app  # noqa: E402
from haverhill_311_function.modules import db  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture()
def scheduler_event():
    """ Generates An Event"""
    return {"body": 'Scheduled event!'}


@pytest.fixture
def qalert_db():
    return db.QAlertDB(
        host='localhost',
        port=5432,
        user='docker',
        password='docker',
        database='qalert_test'
    )


def test_lambda_handler(scheduler_event, qalert_db):
    # clean qalert requests table
    with qalert_db:
        qalert_db.session.query(db.QAlertRequest).delete()
        qalert_db.session.commit()

    # invoke lambda function
    app.lambda_handler(scheduler_event, "")

    # get all qalert request records
    with qalert_db:
        qalert_requests = qalert_db.find_by_props(prop_dict={})

    assert len(qalert_requests) == 5000
