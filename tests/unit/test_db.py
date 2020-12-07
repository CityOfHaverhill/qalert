from haverhill_311_function.modules import settings
from haverhill_311_function.modules import db

import pytest


@pytest.fixture
def qalert_request_repo():
    settings.DB_HOST = 'localhost'
    settings.DB_PORT = 5432
    settings.DB_USER = 'docker'
    settings.DB_PASSWORD = 'docker'
    settings.DB_DATABASE = 'qalert_test'

    return db.create_repo(db.QAlertRequest)


def test_init(qalert_request_repo: db.Repository):
    assert getattr(qalert_request_repo, 'session', None) is None
    assert getattr(qalert_request_repo, 'model', None) == db.QAlertRequest


def test_connection(qalert_request_repo: db.Repository):
    with qalert_request_repo:
        assert(qalert_request_repo.session is not None)


def test_save(qalert_request_repo: db.Repository):
    qalert_request = db.QAlertRequest(
        id=1,
        latitude=1.1,
        longitude=1.1
    )
    with qalert_request_repo:
        qalert_request_repo.save(qalert_request)
        saved_qalert_request = qalert_request_repo.get(entity_id=1)
        assert saved_qalert_request.id == qalert_request.id


def test_save_many(qalert_request_repo: db.Repository):
    qalert_requests = [
        db.QAlertRequest(
            id=1,
            latitude=1.1,
            longitude=1.1
        ),
        db.QAlertRequest(
            id=2,
            latitude=1.1,
            longitude=1.1
        ),
        db.QAlertRequest(
            id=3,
            latitude=1.1,
            longitude=1.1
        ),
    ]
    with qalert_request_repo:
        qalert_request_repo.save_many(qalert_requests)
        assert qalert_request_repo.get(entity_id=1) is not None
        assert qalert_request_repo.get(entity_id=2) is not None
        assert qalert_request_repo.get(entity_id=3) is not None
