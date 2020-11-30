from typing import List

from .modules import db
from .modules import sanitizer
from .modules import qalert

import requests

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes
    """
    data = qalert.pull()

    if type(data) == requests.models.Response:
        return

    latest_date = data[0]["createDate"]

    qalert_requests: List[db.QAlertRequest] = sanitizer.sanitize(
        qalert_data=data
    )
    with db.QAlertDB() as qalert_db:
        try:
            qalert_db.save_many(requests=qalert_requests)
        except Exception as e:
            print(e)

    with db.QAlertAuditDB() as qalert_audit_db:
        latest_qalert_audit = db.QAlertAudit(
            create_date=latest_date
        )
        qalert_audit_db.save(latest_qalert_audit)
