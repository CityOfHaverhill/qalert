from haverhill_311_function import app
from haverhill_311_function.modules import settings
from haverhill_311_function.modules import db

import pytest


@pytest.fixture()
def lambda_event():
    """ Generates An Event"""
    return {}


@pytest.fixture()
def lambda_context():
    """Generates An Context"""
    class Context:
        @staticmethod
        def get_remaining_time_in_millis():
            return 200000

    return Context()


@pytest.fixture
def qalert_request_repo():
    settings.DB_HOST = 'localhost'
    settings.DB_PORT = 5432
    settings.DB_USER = 'docker'
    settings.DB_PASSWORD = 'docker'
    settings.DB_DATABASE = 'qalert_test'

    return db.create_repo(db.QAlertRequest)


def test_lambda_handler(lambda_event, lambda_context, qalert_request_repo: db.Repository):  # noqa: E501
    # clean qalert requests table
    with qalert_request_repo:
        qalert_request_repo.session.query(db.QAlertRequest).delete()
        qalert_request_repo.commit()

    # invoke lambda function
    app.lambda_handler(lambda_event, lambda_context)

    # get all qalert request records
    with qalert_request_repo:
        qalert_requests = qalert_request_repo.find_by(prop_dict={})
    assert len(qalert_requests) == 5000
