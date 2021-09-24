# define methods to operate on data
import re
from typing import Dict

import bs4
from nameparser.parser import HumanName

from src.common.errors.errors import (
    return_none_for_attribute_error,
    return_none_for_index_error,
    return_none_for_type_error,
)
from src.common.network.network import get
from src.common.parser.parser import parse
from src.common.utils.time_it import timeit

from src.shelf.shelf_service import ShelfService
from src.list.list_service import ListService


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

    @return_none_for_type_error
    def get_lists_url(self) -> str:
        lists_url = self.soup.find("a", text="More lists with this book...")["href"]
        return f"{self.GOODREADS_BASE_URL}{lists_url}"

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
    "https://www.goodreads.com/book/show/468488.The_Trick_is_to_Keep_Breathing"
)
response = get([all_the_pretty_horses_url])
soup = parse(response[0])
book_service = BookService(soup)

@timeit
def main():

    title = book_service.get_title()
    series_name = book_service.get_series_name()
    series_uri = book_service.get_series_uri()
    isbn = book_service.get_isbn()
    isbn13 = book_service.get_isbn13()
    year = book_service.get_year_first_published()
    author = book_service.get_author_full_name()
    first = book_service.get_author_first_name(author)
    last = book_service.get_author_last_name(author)
    pages = book_service.get_number_of_pages()
    genres = book_service.get_genres()
    prim_genre = book_service.get_primary_genre(genres)

    # shelf_service = ShelfService(soup)
    # shelves = shelf_service.get_shelves()

    # lists_url = book_service.get_lists_url()
    #
    # response = get([lists_url])
    # soup = parse(response[0])
    # list_service = ListService(soup, lists_url)
    # lists = list_service.get_lists()

    print(
        title,
        series_uri,
        series_name,
        isbn,
        isbn13,
        year,
        author,
        first,
        last,
        pages,
        genres,
        prim_genre,
        # shelves,
        # lists,
    )


# main()
