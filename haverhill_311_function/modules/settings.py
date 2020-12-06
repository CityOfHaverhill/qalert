import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# QAlert settings
QALERT_REQUEST_ENDPOINT = os.environ.get(
    "QALERT_REQUEST_ENDPOINT",
    default="https://haverhillma.qscend.com/qalert/api/v1/requests/get/"
)
QALERT_REQUEST_ENDPOINT_TEST = os.environ.get(
    "QALERT_REQUEST_ENDPOINT_TEST",
    default="http://localhost:8001/api/requests/get"
)
QALERT_API_KEY = os.environ.get(
    "QALERT_API_KEY",
    default="test"
)

# Database settings
DB_HOST = os.environ.get(
    "DB_HOST",
    default="localhost"
)
DB_PORT = os.environ.get(
    "DB_PORT",
    default="5432"
)
DB_USER = os.environ.get(
    "DB_USER",
    default="docker"
)
DB_PASSWORD = os.environ.get(
    "DB_PASSWORD",
    default="docker"
)
DB_DATABASE = os.environ.get(
    "DB_DATABASE",
    default="qalert_test"
)

# Misc settings
TEST = int(os.environ.get(
    "TEST",
    default="1"
))
