import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

URL = os.environ.get("URL")
API_KEY = os.environ.get("API_KEY")
TEST_URL = os.environ.get("TEST_URL")
