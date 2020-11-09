from typing import List

from .modules import db
from .modules import sanitizer
from .modules import qalert


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes
    """
    data = qalert.pull_data_test()
    qalert_requests: List[db.QAlertRequest] = sanitizer.sanitize(
        qalert_data=data
    )
    with db.QAlertDB() as qalert_db:
        latest_date = qalert_requests[0].create_date
        # latest_date should be saved on another Table/Schema as a cache
        qalert_db.save_many(requests=qalert_requests)
