import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
GET_ROLE_URL = os.getenv('GET_ROLE_URL')
GET_USER_URL = os.getenv('GET_USER_URL')
GET_CHANGE_URL = os.getenv('GET_CHANGE_URL')