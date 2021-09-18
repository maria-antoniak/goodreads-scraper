from typing import Union

import bs4
import requests
from requests.models import Response


def get_response(url: str) -> Union[Response, None]:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response
    except requests.ConnectionError:
        return None


def get_soup(response: Union[Response, None]) -> Union[bs4.BeautifulSoup, None]:
    return bs4.BeautifulSoup(response.content, "html.parser")
