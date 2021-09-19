# define methods to operate on data
import re
from typing import Dict
from src.common.utils.time_it import time_it
import pprint

import bs4
from nameparser.parser import HumanName

from src.common.errors.errors import (
    return_none_for_attribute_error,
    return_none_for_index_error,
    return_none_for_type_error,
)
from src.common.network.network import get_response, get_soup


class BookService:
    def __init__(self, soup: bs4.BeautifulSoup):

        self.soup = soup
        self.GOODREADS_BASE_URL = "https://www.goodreads.com"

    @staticmethod
    def get_numeric_id(book_id_title: str) -> int:
        return int(book_id_title.split(".")[0])

    @return_none_for_attribute_error
    def get_title(self) -> str:
        return self.soup.find("h1", {"id": "bookTitle"}).text.strip()

    @return_none_for_attribute_error
    def get_series_name(self) -> str:
        book_series_name = self.soup.find("h2", {"id": "bookSeries"}).text.strip()
        return re.search("[^()]+", book_series_name).group()

    @return_none_for_attribute_error
    @return_none_for_type_error
    def get_series_uri(self) -> str:
        h2 = self.soup.find_all("h2", {"id": "bookSeries"})
        for node in h2:
            uri = node.find("a")["href"]
            return f"{self.GOODREADS_BASE_URL}{uri}"

    @return_none_for_index_error
    def get_isbn(self) -> int:
        isbn = re.findall("isbn: [0-9]{10}", str(self.soup))
        return int(isbn[0].split()[1])

    @return_none_for_index_error
    def get_isbn13(self) -> int:
        isbn13 = re.findall(r"isbn13: [0-9]{13}", str(self.soup))
        return int(isbn13[0].split()[1])

    @return_none_for_attribute_error
    def get_year_first_published(self) -> int:
        year_first_published = self.soup.find(
            "nobr", attrs={"class": "greyText"}
        ).string.strip()
        return int(re.search("([0-9]{3,4})", year_first_published).group())

    @return_none_for_attribute_error
    def get_author_full_name(self):
        return self.soup.find("a", {"class": "authorName"}).text.strip()

    @staticmethod
    def get_author_first_name(author_full_name: str) -> str:
        return HumanName(author_full_name).first

    @staticmethod
    def get_author_last_name(author_full_name: str) -> str:
        return HumanName(author_full_name).last

    @return_none_for_attribute_error
    def get_number_of_pages(self) -> int:
        num_pages = self.soup.find("span", {"itemprop": "numberOfPages"}).text.strip()
        return int(num_pages.split()[0])

    @return_none_for_attribute_error
    def get_genres(self) -> [str]:
        genres = []
        for node in self.soup.find_all("div", {"class": "left"}):
            current_genres = node.find_all(
                "a", {"class": "actionLinkLite bookPageGenreLink"}
            )
            current_genre = " > ".join([g.text for g in current_genres])
            if current_genre.strip():
                genres.append(current_genre)
        return genres

    @staticmethod
    @return_none_for_index_error
    def get_primary_genre(genre_list: [str]) -> str:
        # This is according to the genres with most votes
        return genre_list[0]

    # TODO: Consider breaking shelves into a service.

    @return_none_for_type_error
    def _get_shelves_url(self):
        shelves_url = self.soup.find("a", text="See top shelves…")["href"]
        return f"{self.GOODREADS_BASE_URL}{shelves_url}"

    @staticmethod
    @return_none_for_index_error
    def _get_unformatted_shelves(soup: bs4.BeautifulSoup) -> [str]:
        nodes = soup.find_all("div", {"class": "shelfStat"})
        return [" ".join(node.text.strip().split()) for node in nodes]

    def get_shelves(self) -> Dict:
        # TODO: This method needs an integration test!

        shelves = {}

        url = BookService._get_shelves_url(self)

        response = get_response(url)
        soup = get_soup(response)

        for shelf in BookService._get_unformatted_shelves(soup):
            name = BookService._get_shelf_name(shelf)
            count = BookService._get_shelf_count(shelf)
            shelves[name] = count

        return shelves

    @staticmethod
    def _get_shelf_name(shelf: str) -> str:
        return shelf.split()[:-2][0]

    @staticmethod
    def _get_shelf_count(shelf: str) -> int:
        return int(shelf.split()[-2].replace(",", ""))

    # TODO: Consider breaking lists into a service.

    @return_none_for_type_error
    def _get_lists_url(self) -> str:
        lists_url = self.soup.find("a", text="More lists with this book...")["href"]
        return f"{self.GOODREADS_BASE_URL}{lists_url}"

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
    def _get_unformatted_lists(url) -> [str]:
        response = get_response(url)
        soup = get_soup(response)
        return [node.text for node in soup.find_all("div", {"class": "cell"})]

    @return_none_for_index_error
    def _get_unformatted_lists_handler(self) -> [str]:
        lists = []

        url = BookService._get_lists_url(self)
        response = get_response(url)
        soup = get_soup(response)
        paginated_urls = BookService._get_paginated_list_urls(soup, url)

        for url in paginated_urls:
            response = get_response(url)
            soup = get_soup(response)
            lists += [node.text for node in soup.find_all("div", {"class": "cell"})]
        return lists

    @staticmethod
    def _split_list_details(_list):
        return _list.strip().split("\n")

    @staticmethod
    def _get_list_name_from_list_details(_list):
        return _list[0]

    @staticmethod
    def _get_list_rank_from_list_details(_list) -> int:
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

    @time_it
    def get_lists(self) -> [Dict]:
        # TODO: This method needs an integration test!
        """
        Initial baseline was 33 secs, now down to 16
        """
        list_count_dict = []

        for _list in BookService._get_unformatted_lists_handler(self):
            list_details = BookService._split_list_details(_list)

            list_name = BookService._get_list_name_from_list_details(list_details)
            list_votes = BookService._get_list_votes_from_list_details(list_details)
            list_rank = BookService._get_list_rank_from_list_details(list_details)
            number_of_books_on_list = (
                BookService._get_number_of_books_on_list_from_list_details(list_details)
            )

            list_count_dict.append(
                {
                    "listName": list_name,
                    "listVotes": list_votes,
                    "listRank": list_rank,
                    "numberOfBooksOnList": number_of_books_on_list,
                }
            )

        return BookService._sort_by_list_votes(list_count_dict)

    @staticmethod
    def _sort_by_list_votes(lists: [Dict]) -> [Dict]:
        # This mimics the UI on Goodreads
        return sorted(lists, key=lambda k: k["listVotes"], reverse=True)

    @return_none_for_attribute_error
    def get_number_of_reviews(self) -> str:
        return self.soup.find("meta", {"itemprop": "reviewCount"})["content"].strip()

    @return_none_for_attribute_error
    def get_number_of_ratings(self) -> str:
        return self.soup.find("meta", {"itemprop": "reviewCount"})["content"].strip()

    @return_none_for_attribute_error
    def get_average_rating(self) -> str:
        return self.soup.find("span", {"itemprop": "ratingValue"}).text.strip()

    @return_none_for_attribute_error
    def get_rating_distribution(self) -> Dict:
        distribution = re.findall(r"renderRatingGraph\([\s]*\[[0-9,\s]+", str(soup))[0]
        distribution = " ".join(distribution.split())
        distribution = [int(c.strip()) for c in distribution.split("[")[1].split(",")]
        distribution_dict = {
            "5 Stars": distribution[0],
            "4 Stars": distribution[1],
            "3 Stars": distribution[2],
            "2 Stars": distribution[3],
            "1 Star": distribution[4],
        }
        return distribution_dict


# TESTING

all_the_pretty_horses_url = (
    "https://www.goodreads.com/book/show/469571.All_the_Pretty_Horses"
)
response = get_response(all_the_pretty_horses_url)
soup = get_soup(response)
book_service = BookService(soup)

