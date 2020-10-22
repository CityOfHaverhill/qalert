from haverhill_311_function.modules import db


def test_init():
    qalert_db = db.QAlertDB(
        host='host',
        port=5000,
        user='user',
        password='password',
        region='region',
        database='database'
    )

    assert getattr(qalert_db, 'conn', None) is None
    assert qalert_db.host == 'host'
    assert qalert_db.port == 5000
    assert qalert_db.user == 'user'
    assert qalert_db.password == 'password'
    assert qalert_db.database == 'database'
