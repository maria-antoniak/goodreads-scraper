import math
import re
from typing import Dict, Union

import bs4
from nameparser.parser import HumanName

from src.common.errors.errors import (return_none_for_attribute_error,
                                      return_none_for_index_error,
                                      return_none_for_type_error)
from src.common.utils.dict_operators import sort_by_value
from src.common.utils.string_operators import split_on_delimiter


class BookService:
    def __init__(self, soup: bs4.BeautifulSoup):

        self.soup = soup
        self.GOODREADS_BASE_URL = "https://www.goodreads.com"

    @staticmethod
    def get_numeric_id(book_id_title: str) -> [int, None]:
        try:
            return int(split_on_delimiter(book_id_title, "."))
        except ValueError:
            return int(split_on_delimiter(book_id_title, "-"))

    @return_none_for_attribute_error
    def get_title(self) -> str:
        return self.soup.find("h1", {"id": "bookTitle"}).text.strip()

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
    def get_year_of_publication(self) -> int:
        year_of_publication = self.soup.find(
            "nobr", attrs={"class": "greyText"}
        ).string.strip()
        return int(re.search("([0-9]{3,4})", year_of_publication).group())

    @staticmethod
    @return_none_for_type_error
    def get_century_of_publication(year_of_publication: int) -> int:
        return math.ceil(year_of_publication / 100)

    @return_none_for_attribute_error
    def get_genres(self) -> [str]:
        # TODO: It might be nice build a list of dicts considering the votes here.
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
    @return_none_for_type_error
    def get_primary_genre(genre_list: [str]) -> str:
        # The genre with most votes
        return genre_list[0]

    @return_none_for_attribute_error
    def get_series_name(self) -> str:
        book_series_name = self.soup.find("h2", {"id": "bookSeries"}).text.strip()
        match = re.search("[^()]+", book_series_name).group()
        return match.strip()

    @return_none_for_attribute_error
    @return_none_for_type_error
    def get_series_url(self) -> str:
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

    @return_none_for_type_error
    @return_none_for_attribute_error
    def get_lists_url(self) -> str:
        lists_url = self.soup.find("a", text="More lists with this book...")["href"]
        return f"{self.GOODREADS_BASE_URL}{lists_url}"

    @return_none_for_type_error
    @return_none_for_attribute_error
    def get_number_of_reviews(self) -> Union[int, None]:
        value = self.soup.find("meta", {"itemprop": "reviewCount"})["content"].strip()
        return int(value)

    @return_none_for_type_error
    @return_none_for_attribute_error
    def get_number_of_ratings(self) -> Union[int, None]:
        value = self.soup.find("meta", {"itemprop": "ratingCount"})["content"].strip()
        return int(value)

    @return_none_for_attribute_error
    def get_average_rating(self) -> Union[float, None]:
        value = self.soup.find("span", {"itemprop": "ratingValue"}).text.strip()
        f = float(value)
        return round(f, 2)


    @return_none_for_attribute_error
    def get_rating_distribution(self) -> Dict[str, int]:
        distribution = re.findall(
            r"renderRatingGraph\([\s]*\[[0-9,\s]+", str(self.soup)
        )[0]
        distribution = " ".join(distribution.split())
        distribution = [int(c.strip()) for c in distribution.split("[")[1].split(",")]
        result = {
            "fiveStar": distribution[0],
            "fourStar": distribution[1],
            "threeStar": distribution[2],
            "twoStar": distribution[3],
            "oneStar": distribution[4],
        }

        return dict(sort_by_value(result))

    @return_none_for_type_error
    def _get_shelves_url(self) -> str:
        shelves_url = self.soup.find("a", text="See top shelves…")["href"]
        return f"{self.GOODREADS_BASE_URL}{shelves_url}"
