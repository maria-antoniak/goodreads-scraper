from typing import Union

import bs4
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


def parse_book(book_id: str, parser=None):
    URL = f"https://www.goodreads.com/book/show/{book_id}"
    return bs4.BeautifulSoup(get(URL).content, "html.parser")
