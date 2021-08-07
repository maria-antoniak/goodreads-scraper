from typing import Union

import requests
from requests.models import Response


def get(url: str) -> Union[Response, None]:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response
    except requests.ConnectionError:
        return None
