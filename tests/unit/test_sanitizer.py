from datetime import datetime
from haverhill_311_function.modules.sanitizer import QAlertRequestSchema
from haverhill_311_function.modules.sanitizer import sanitize_many
import pytest


@pytest.fixture
def qalert_data():
    return [{"id": 106472,
             "status": 0,
             "createDate": "10/9/2020 10:58 AM",
             "priorityToDisplay": 2,
             "createDateUnix": 1602255480,
             "lastAction": "10/9/2020 10:58 AM",
             "lastActionUnix": 1602255480,
             "typeId": 300,
             "typeName": "Overgrown Grass/Weeds",
             "hasLinks": False,
             "comments": "Yard is a mess!\nOvergrown grass and trash alongside of garage.",  # noqa: E501
             "streetNum": "10",
             "streetName": "PEAR TREE RD",
             "crossName": "",
             "cityName": "Haverhill",
             "latitude": 42.7989995,
             "longitude": -71.05045,
             "name": "MIKE COSTA",
             "email": "mikecosta3065@gmail.com"
             }]


@pytest.fixture
def qalert_requests():
    return sanitize_many([{"id": 106472,
                      "status": 0,
                      "createDate": "10/9/2020 10:58 AM",
                      "priorityToDisplay": 2,
                      "createDateUnix": 1602255480,
                      "lastAction": "10/9/2020 10:58 AM",
                      "lastActionUnix": 1602255480,
                      "typeId": 300,
                      "typeName": "Overgrown Grass/Weeds",
                      "hasLinks": False,
                      "comments": "Yard is a mess!\nOvergrown grass and trash alongside of garage.",  # noqa: E501
                      "streetNum": "10",
                      "streetName": "PEAR TREE RD",
                      "crossName": "",
                      "cityName": "Haverhill",
                      "latitude": 42.7989995,
                      "longitude": -71.05045,
                      "name": "MIKE COSTA",
                      "email": "mikecosta3065@gmail.com"}])


def test_schema(qalert_data):
    for i in qalert_data:
        schema = QAlertRequestSchema()
        data = schema.load(i)
        assert type(data['id']) == int
        assert type(data['status']) == int
        assert type(data['create_date']) == datetime
        assert type(data['create_date_unix']) == int
        assert type(data['last_action']) == datetime
        assert type(data['last_action_unix']) == int
        assert type(data['type_id']) == int
        assert type(data['type_name']) == str
        assert type(data['comments']) == str
        assert type(data['street_num']) == str
        assert type(data['street_name']) == str
        assert type(data['cross_name']) == str
        assert type(data['city_name']) == str
        assert type(data['longitude']) == float
        assert type(data['latitude']) == float


def test_schema_ignore_unknown(qalert_data):
    schema = QAlertRequestSchema()
    for qalert_request_data in qalert_data:
        qalert_request_data['a'] = 1
        data = schema.dump(qalert_request_data)
        assert 'a' not in data


def test_removed_pii(qalert_requests):
    schema = QAlertRequestSchema()
    for i in qalert_requests:
        data = schema.dump(i)
        assert len(data) == 15
        assert 'name' not in data
        assert 'email' not in data


def test_sanitization(qalert_data):
    for i in qalert_data:
        assert len(i) == 19
