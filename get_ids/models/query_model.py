from dataclasses import dataclass
from typing import Union


@dataclass
class QueryModel:
    book_title: str
    author_name: str
    book_title_minus_subtitle: Union[str, None]
    book_title_and_author_name_search_url: str
    book_title_search_url: str
    book_title_minus_subtitle_search_url: Union[str, None]
