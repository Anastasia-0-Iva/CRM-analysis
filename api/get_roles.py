import datetime

import requests

from config.main_config import API_KEY, GET_USER_URL
from utils.get_signatures_for_api import get_signature

print(API_KEY)

data = {'timestamp': int(datetime.datetime.now().timestamp())}
signature = get_signature(data, API_KEY)
response = requests.post(
    url=GET_USER_URL,
    json=data,
    headers={'Authorization': signature}
)
print(response.status_code)
print(response.json())
