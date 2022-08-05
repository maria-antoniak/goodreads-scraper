# TODO Figure out why this service is failing

from typing import Dict

import bs4

from src.common.errors.errors import (return_none_for_assertion_error,
                                      return_none_for_index_error)
from src.shelf.shelf_config import *


class ShelfService:
    def __init__(self, soup: bs4.BeautifulSoup):

        self.soup = soup
        self.GOODREADS_BASE_URL = "https://www.goodreads.com"

    def get_shelves(self) -> [Dict]:
        #  The amount of results returned is dependent on `config_number_of_shelf_results`

        shelves = []

        for shelf in ShelfService._get_unformatted_shelves(self):
            name = ShelfService._get_shelf_name(shelf)
            count = ShelfService._get_shelf_count(shelf)

            shelves.append(
                {"shelfName": name, "AmountOfUsersWhoAddedBookToShelf": count}
            )

        return shelves[:config_number_of_shelf_results]

    def _get_unformatted_shelves(self) -> [str]:
        nodes = self.soup.find_all("div", {"class": "shelfStat"})
        return [" ".join(node.text.strip().split()) for node in nodes]

    @staticmethod
    def _get_shelf_name(shelf: str) -> str:
        return shelf.split()[:-2][0]

    @staticmethod
    def _get_shelf_count(shelf: str) -> int:
        return int(shelf.split()[-2].replace(",", ""))
