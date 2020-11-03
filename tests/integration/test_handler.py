from typing import List
import os

os.environ.update({
    "URL": "blah",
    "API_KEY": "blah",
    "TEST_URL": "https://qalert-data.s3.us-east-2.amazonaws.com/requests_get.json",
    "db_host": "localhost",
    "db_port": "5432",
    "db_user": "docker",
    "db_password": "docker",
    "db_database": "qalert_test"
})

from haverhill_311_function import app
from haverhill_311_function.modules import db

import pytest


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
