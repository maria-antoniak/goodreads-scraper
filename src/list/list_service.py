import re
from typing import Dict

import bs4

from src.common.errors.errors import return_none_for_index_error, return_none_for_type_error
from src.common.network.network import get
from src.common.parser.parser import parse
from src.list.list_config import *


class ListService:
    def __init__(self, soup: bs4.BeautifulSoup, lists_url: str):

        self.soup = soup
        self.lists_url = lists_url
        self.GOODREADS_BASE_URL = "https://www.goodreads.com"

    @return_none_for_type_error
    def get_lists(self) -> [Dict]:
        # TODO: This method needs an integration test!
        """
        Initial baseline was 33 secs, now down to 16
        As of introducing async we're down to 5 seconds
        """
        lists = []

        response = get([self.lists_url])
        soup = parse(response[0])
        paginated_urls = ListService._get_paginated_list_urls(soup, self.lists_url)

        for _list in ListService._get_unformatted_lists_handler(paginated_urls):
            list_details = ListService._split_list_details(_list)

            list_name = ListService._get_list_name_from_list_details(list_details)
            list_votes = ListService._get_list_votes_from_list_details(list_details)
            book_rank_in_list = ListService._get_book_rank_in_list_from_list_details(
                list_details
            )
            number_of_books_on_list = (
                ListService._get_number_of_books_on_list_from_list_details(list_details)
            )

            lists.append(
                {
                    "listName": list_name,
                    "listVotes": list_votes,
                    "bookRankInList": book_rank_in_list,
                    "numberOfBooksOnList": number_of_books_on_list,
                }
            )

        result = ListService._sort_by_list_votes(lists)
        return result[:config_number_of_list_results]

    @staticmethod
    def _get_paginated_list_urls(soup: bs4.BeautifulSoup, lists_url: str) -> [str]:
        paginated_list_urls = [lists_url]
        soup.find_all("a", href=re.compile("/list/book/"))
        amount = len(
            soup.find_all("a", href=lambda href: href and "/list/book/" in href)[:-1]
        )
        if amount:
            for i in range(2, amount + 2):
                paginated_list_urls.append(f"{lists_url}{'?page='}{i}")
            return paginated_list_urls
        return None

    @staticmethod
    def _get_res_for_paginated_lists(paginated_list_urls: [str]):
        return get(paginated_list_urls)

    @staticmethod
    @return_none_for_index_error
    def _get_unformatted_lists_handler(paginated_list_urls: [str]) -> [str]:
        lists = []

        for response in ListService._get_res_for_paginated_lists(paginated_list_urls):
            soup = parse(response)
            lists += [node.text for node in soup.find_all("div", {"class": "cell"})]
        return lists

    @staticmethod
    def _split_list_details(_list):
        return _list.strip().split("\n")

    @staticmethod
    def _get_list_name_from_list_details(_list):
        return _list[0]

    @staticmethod
    def _get_book_rank_in_list_from_list_details(_list) -> int:
        raw = "".join(_list[2]).strip()
        return int(re.search(r"(\d+)(.+out of)", raw).group(1))

    @staticmethod
    def _get_list_votes_from_list_details(_list) -> int:
        raw = "".join(_list[-1])
        raw = raw.strip().replace(",", "")
        raw = re.sub(r"\s(voters|voter)", "", raw)
        return int(raw)

    @staticmethod
    def _get_number_of_books_on_list_from_list_details(_list) -> int:
        raw = "".join(_list[2]).strip().replace(",", "")
        return int(re.search(r"(\d+)(\s)(books)", raw).group(1))

    @staticmethod
    def _sort_by_list_votes(lists: [Dict]) -> [Dict]:
        # This mimics the UI on Goodreads
        return sorted(lists, key=lambda k: k["listVotes"], reverse=True)
