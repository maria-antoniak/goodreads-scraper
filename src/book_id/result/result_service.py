import re
from typing import Union

import bs4
from bs4 import BeautifulSoup

from src.common.errors.errors import (return_none_for_assertion_error,
                                      return_none_for_attribute_error,
                                      return_none_for_type_error)


class ResultService:
    def __init__(self, soup: Union[BeautifulSoup, None]):

        self.soup = soup

    @return_none_for_assertion_error
    @return_none_for_attribute_error
    def get_results(self) -> [bs4.element.ResultSet, []]:
        return self.soup.find_all("tr", {"itemtype": "http://schema.org/Book"})

    @staticmethod
    @return_none_for_attribute_error
    def _get_book_title(results: [bs4.element.ResultSet, None]) -> Union[str, None]:
        return results.find("a", {"class": "bookTitle"}).text.strip()

    @staticmethod
    @return_none_for_attribute_error
    def _get_author_name(results: [bs4.element.ResultSet, None]) -> Union[str, None]:
        return (
            results.find("div", {"class": "authorName__container"})
            .text.strip()
            .rstrip(",")
        )

    @staticmethod
    @return_none_for_type_error
    def _clean_author_name(author_name: Union[str, None]) -> str:
        goodreads_author_parenthesis = "(Goodreads Author)"
        if goodreads_author_parenthesis in author_name:
            return author_name.replace(goodreads_author_parenthesis, "").strip()
        return author_name.strip()

    @staticmethod
    @return_none_for_attribute_error
    @return_none_for_type_error
    def _get_book_href(results: [bs4.element.ResultSet, None]) -> Union[str, None]:
        return results.find("a", {"class": "bookTitle"})["href"]

    @staticmethod
    @return_none_for_attribute_error
    @return_none_for_type_error
    def _get_id_from_href(href: Union[str, None]) -> Union[str, None]:
        pattern = re.compile(r"(/book/show/)(.+)(\?)")
        return pattern.search(href).group(2)
