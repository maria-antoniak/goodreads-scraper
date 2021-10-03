import re
import urllib
from typing import Union
from urllib import parse

from src.book_id.query.query_config import *


class QueryService:
    def __init__(self, query: Union[str, None]):

        self.query = query

    def _split_on_last_delimiter(self) -> [str]:
        split = self.query.rsplit(config_delimiter, 1)
        return [query.strip() for query in split]

    @staticmethod
    def _is_subtitle_in_book_title(book_title: str) -> bool:
        subtitles = [": ", "; ", " ("]
        if any(subtitle in book_title for subtitle in subtitles):
            return True
        return False

    @staticmethod
    def _remove_subtitle_from_book_title(book_title: str) -> str:
        subtitle_pattern = re.compile(r"(:|;|\s\().+")
        return re.sub(subtitle_pattern, "", book_title)

    @staticmethod
    def _build_search_url_from_query(query: str) -> Union[str, None]:
        if query is None:
            return None

        base_url = "https://www.goodreads.com/search?q="
        return f"{base_url}{urllib.parse.quote(query)}"
