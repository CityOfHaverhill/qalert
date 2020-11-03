from haverhill_311_function.modules import db

import pytest


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
