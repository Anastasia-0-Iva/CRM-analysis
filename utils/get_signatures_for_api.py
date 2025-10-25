import hashlib
import json
from typing import Any


def get_signature(request_body: dict[str, Any], api_key: str) -> str:
    json_data = json.dumps(request_body)
    return hashlib.sha1((json_data + api_key).encode('utf-8')).hexdigest()


