from .modules import db
from .modules import qalert
from .modules import sanitizer
from .modules import utils


# latest_date is used to keep track of what the latest 311 request from
# QAlert saved to the database was.
latest_date: str = None


def lambda_handler(event, context):
    """Lambda function handler

    Parameters
    ----------
    event: dict, required
        Lambda Input Format

    context: object, required
        Lambda Context runtime methods and attributes
    """
    # Timeout run_pipeline function 20 seconds before the lambda is
    # terminated so that we can do nessesary work cleanup before lambda
    # gets terminated
    pipeline_timeout = get_lambda_timeout(context) - 20
    # Run the pipeline to retreive QAlert data and store in database
    run_pipeline(timeout=pipeline_timeout)


def get_lambda_timeout(lambda_context) -> int:
    """Gets the remaining lambda execution time in seconds."""
    return int(lambda_context.get_remaining_time_in_millis()/1000)


def run_pipeline(timeout: int):
    """Core data pipeline logic.
    Parameters
    ----------
    timeout: int, required
        Number of seconds after which the pipeline must terminate.

    Notes
    ----------
    pipeline execution steps:
        1. pull new 311 requests from QAlert in acending order of creation date (oldest first)
        2. for each new 311 request returned from QAlert do steps 3-5 (until completion or timeout is reached)
        3. santitize the raw 311 request by removing pii and loading into a QAlertRequest instance
        4. save and commit the QAlertRequest instance
        5. update the global latest_date variable with the creation date of the saved QAlertRequest
    """
    global latest_date

    qalert_request_repo = db.create_repo(entity_model=db.QAlertRequest)
    audit_repo = db.create_repo(entity_model=db.QAlertAudit)

    try:
        with utils.Timeout(seconds=timeout):
            # Connect to database
            qalert_request_repo.connect()
            audit_repo.connect()
            # Pull new 311 requests from QAlert
            data = qalert.pull()
            # Process 311 requests one by one
            for qalert_request_data in data:
                process_qalert_request(qalert_request_data, qalert_request_repo)
    except TimeoutError:
        # Function was not able to complete within alloted time
        print('Function timed out before completing but was handled. Saving progress.')
    finally:
        if latest_date:
            # Save progress (last 311 request from QAlert saved) so that next
            # lambda invokation can pick up where this invokation left off
            latest_qalert_audit = db.QAlertAudit(
                create_date=latest_date
            )
            audit_repo.save(entity=latest_qalert_audit)
        # Cleanup resources
        audit_repo.disconnect()
        qalert_request_repo.disconnect()


def process_qalert_request(qalert_request_data: dict, qalert_request_repo: db.Repository):
    """Sanitize and save a 311 request from QAlert to database.
    
    Parameters
    ----------
    qalert_request_data: dict, required
        A 311 request retreived from QAlert API.
    
    qalert_request_repo: Repository, required
        A Repository bound to the QAlertRequest model.
    """
    global latest_date

    try:
        qalert_request = sanitizer.sanitize(
            qalert_data=qalert_request_data
        )
        qalert_request_repo.save(entity=qalert_request)
        latest_date = qalert_request_data['createDate']
    except (sanitizer.SanitizeException, db.DBException) as exc:
        print(f'Exception processing a qalert 311 request: {exc}')
