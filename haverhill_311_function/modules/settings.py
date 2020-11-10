import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# QAlert settings
QALERT_REQUEST_ENDPOINT = os.environ.get("QALERT_REQUEST_ENDPOINT")
QALERT_REQUEST_ENDPOINT_TEST = os.environ.get("QALERT_REQUEST_ENDPOINT_TEST")
QALERT_API_KEY = os.environ.get("QALERT_API_KEY")

# Database settings
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")

# Misc settings
TEST = os.environ.get("TEST")
