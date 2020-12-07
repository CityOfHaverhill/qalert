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
        qalert_request = QAlertRequest(
            id=qalert_request_validated.get('id'),
            status=qalert_request_validated.get('status'),
            create_date=qalert_request_validated.get('create_date'),
            create_date_unix=qalert_request_validated.get('create_date_unix'),
            last_action=qalert_request_validated.get('last_action'),
            last_action_unix=qalert_request_validated.get('last_action_unix'),
            type_id=qalert_request_validated.get('type_id'),
            type_name=qalert_request_validated.get('type_name'),
            comments=qalert_request_validated.get('comments'),
            street_num=qalert_request_validated.get('street_num'),
            cross_name=qalert_request_validated.get('cross_name'),
            city_name=qalert_request_validated.get('city_name'),
            latitude=qalert_request_validated.get('latitude'),
            longitude=qalert_request_validated.get('longitude')
        )
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
