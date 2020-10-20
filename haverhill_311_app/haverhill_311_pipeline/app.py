import haverhill_311_app.haverhill_311_pipeline.modules.qalert as qalert
import haverhill_311_app.haverhill_311_pipeline.modules.sanitizer as sanitizer
import haverhill_311_app.haverhill_311_pipeline.modules.db as db


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
    # data = qalert.pull()
    # sanitizer.sanitize(data)
    # db.insert(processed_data)
