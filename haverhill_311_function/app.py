from .modules import db
from .modules import qalert
from .modules import sanitizer

from func_timeout import func_timeout, FunctionTimedOut


latest_date: str = None


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes
    """
    try:
        # timeout run_pipeline function after 80 seconds so that we can do
        # nessesary work cleanup before lambda gets terminated
        func_timeout(timeout=80, func=run_pipeline)
    except FunctionTimedOut:
        print('Function timed out before completing but was handled')
    finally:
        if latest_date:
            with db.QAlertAuditDB() as qalert_audit_db:
                latest_qalert_audit = db.QAlertAudit(
                    create_date=latest_date
                )
                qalert_audit_db.save(latest_qalert_audit)


def run_pipeline():
    global latest_date

    data = qalert.pull()
    with db.QAlertDB() as qalert_db:
        for qalert_request_data in data:
            try:
                qalert_request = sanitizer.sanitize(
                    qalert_data=qalert_request_data
                )
                qalert_db.save(request=qalert_request)
                latest_date = qalert_request_data['createDate']
            except Exception as exc:
                print(f'Exception processing qalert_request: {exc}')
                continue
