# import os
from haverhill_311_function.modules import settings
from haverhill_311_function.modules import qalert

import typing
import pytest
import json


def test_valid_format():
    settings.TEST = True
    res = qalert.pull()
    print(res)
    # assert res)) == typing.List[dict]


def test_using_endpoint():
    settings.TEST = True
    res = qalert.pull()
    assert res is not None


def test_actual_endpoint():
    settings.TEST = False
    res = qalert.pull()
    assert res == []
