import re
from typing import Union

import bs4
from bs4 import BeautifulSoup

from get_ids.errors.errors import (return_none_for_attribute_error,
                           return_none_for_type_error)


@return_none_for_attribute_error
def get_results(soup: [BeautifulSoup, None]) -> [bs4.element.ResultSet, None]:
    return soup.find_all("tr", {"itemtype": "http://schema.org/Book"})


@return_none_for_attribute_error
def _get_book_title(soup: BeautifulSoup) -> str:
    return soup.find("a", {"class": "bookTitle"}).text.strip()


@return_none_for_attribute_error
def _get_author_name(soup: BeautifulSoup) -> str:
    return soup.find("div", {"class": "authorName__container"}).text.strip().rstrip(",")


@return_none_for_type_error
def _clean_author_name(author_name: Union[str, None]) -> str:
    goodreads_author_parenthesis = "(Goodreads Author)"
    if goodreads_author_parenthesis in author_name:
        return author_name.replace(goodreads_author_parenthesis, "").strip()
    return author_name.strip()


@return_none_for_type_error
def _get_book_href(soup: BeautifulSoup) -> str:
    return soup.find("a", {"class": "bookTitle"})["href"]


@return_none_for_attribute_error
@return_none_for_type_error
def _get_id_from_href(href: Union[str, None]) -> Union[str, None]:
    pattern = re.compile(r"(/book/show/)(.+)(\?)")
    return pattern.search(href).group(2)
