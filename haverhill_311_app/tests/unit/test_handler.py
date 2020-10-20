import pytest

from haverhill_311_app.haverhill_311_pipeline import app


@pytest.fixture()
def scheduler_event():
    """ Generates An Event"""
    return {"body": 'Scheduled event!'}


def test_lambda_handler(scheduler_event, mocker):
    ret = app.lambda_handler(scheduler_event, "")
    assert ret
