from haverhill_311_function.modules import qalert

import pytest
import json


def check_valid_format():
    os.environ["TEST"] = True
    res = qalert.pull()
    assert type(json.loads(res)) == dict

def check_using_test_endpoint():
    os.environ["TEST"] = True
    res = qalert.pull()
    assert res is not None

def check_actual_endpoint():
    os.environ["TEST"] = False
    res = qalert.pull()
    assert res.status_code == 404