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

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    """
    data = qalert.pull_data_test()
    qalert_requests: List[db.QAlertRequest] = sanitizer.sanitize(qalert_data=data)
    with db.QAlertDB() as qalert_db:
        qalert_db.save_many(requests=qalert_requests)
