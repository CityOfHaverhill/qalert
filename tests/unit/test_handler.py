import pytest

from haverhill_311_function import app


@pytest.fixture()
def scheduler_event():
    """ Generates An Event"""
    return {"body": 'Scheduled event!'}


def test_lambda_handler(scheduler_event, mocker):
    pass
