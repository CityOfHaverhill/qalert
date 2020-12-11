"""The sanitizer module cleans and processes 311 data retreived from QAlert
    in preperation for storage in db.
"""
from typing import List

from .db import QAlertRequest

from marshmallow import EXCLUDE, Schema
from marshmallow.exceptions import MarshmallowError
from marshmallow.fields import DateTime, Integer, String, Float


class SanitizeException(Exception):
    """Base exception for sanitizer module."""


class QAlertRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    id = Integer(required=True)
    status = Integer()
    create_date = DateTime(r"%m/%d/%Y %I:%M %p", data_key='createDate')
    create_date_unix = Integer(data_key='createDateUnix')
    last_action = DateTime(r"%m/%d/%Y %I:%M %p", data_key='lastAction')
    last_action_unix = Integer(data_key='lastActionUnix')
    type_id = Integer(data_key='typeId')
    type_name = String(data_key='typeName')
    comments = String(data_key='comments')
    street_num = String(data_key='streetNum')
    street_name = String(data_key='streetName')
    cross_name = String(data_key='crossName')
    city_name = String(data_key='cityName')
    latitude = Float(data_key='latitude', required=True)
    longitude = Float(data_key='longitude', required=True)


def sanitize(qalert_data: dict) -> QAlertRequest:
    try:
        qalert_request_schema = QAlertRequestSchema()
        qalert_request_validated = qalert_request_schema.load(
            qalert_data
        )
        qalert_request = QAlertRequest(**qalert_request_validated)
        return qalert_request
    except MarshmallowError as exc:
        raise SanitizeException(exc)


def sanitize_many(qalert_data: List[dict], ignore_exceptions=True) -> List[QAlertRequest]:  # noqa: E501
    qalert_requests = []
    for qalert_request_data in qalert_data:
        try:
            qalert_request = sanitize(qalert_request_data)
            qalert_requests.append(qalert_request)
        except SanitizeException as exc:
            if ignore_exceptions:
                continue
            raise exc
    return qalert_requests
