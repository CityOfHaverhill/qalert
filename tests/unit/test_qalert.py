from haverhill_311_function.modules import settings
from haverhill_311_function.modules import qalert


def test_valid_format():
    settings.TEST = True
    res = qalert.pull()
    assert type(res) == list
    assert type(res[0]) == dict


def test_using_endpoint():
    settings.TEST = True
    res = qalert.pull()
    assert res is not None


def test_actual_endpoint():
    settings.TEST = False
    res = qalert.pull()
    print(res)
    assert res == []
