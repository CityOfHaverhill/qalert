from .modules import db
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
    processed_data = []
    for record in data:
        processed_record = {
            'id': record['id'],
            'latitude': record['latitude'],
            'longitude': record['longitude'],
            'typeId': record['typeId'],
            'typeName': record['typeName'] 
        }
        processed_data.append(processed_record)
    qalert_db = db.QAlertDB()
    with qalert_db:
        qalert_db.insert_many(records=processed_data)
