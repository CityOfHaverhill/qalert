import os

os.environ['TEST'] = '1'

from haverhill_311_function.modules import db  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture
def qalert_db():
    return db.QAlertDB(
        host='localhost',
        port=5432,
        user='docker',
        password='docker',
        database='qalert_test'
    )


def test_init(qalert_db):
    assert getattr(qalert_db, 'session', None) is None
    assert qalert_db.host == 'localhost'
    assert qalert_db.port == 5432
    assert qalert_db.user == 'docker'
    assert qalert_db.password == 'docker'
    assert qalert_db.database == 'qalert_test'


def test_connection(qalert_db):
    with qalert_db:
        assert(qalert_db.session is not None)


def test_save(qalert_db):
    qalert_request = db.QAlertRequest(
        id=1,
        latitude=1.1,
        longitude=1.1
    )
    with qalert_db:
        qalert_db.save(qalert_request)
        saved_qalert_request = qalert_db.get(request_id=1)
        assert saved_qalert_request == qalert_request


def test_save_many(qalert_db):
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
    with qalert_db:
        qalert_db.save_many(qalert_requests)
        assert qalert_db.get(request_id=1) is not None
        assert qalert_db.get(request_id=2) is not None
        assert qalert_db.get(request_id=3) is not None
