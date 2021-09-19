# define methods to operate on data

import re
from src.common.network.network import get_response, get_soup
import bs4
from src.common.errors.errors import return_none_for_attribute_error, return_none_for_type_error, return_none_for_index_error
from typing import Dict
import time
from nameparser.parser import HumanName


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
        h2 = self.soup.find_all('h2', {'id': 'bookSeries'})
        for node in h2:
            uri = node.find('a')['href']
            return f"{self.GOODREADS_BASE_URL}{uri}"

    @return_none_for_index_error
    def get_isbn(self) -> str:
        isbn = re.findall('isbn: [0-9]{10}', str(self.soup))
        return isbn[0].split()[1]

    @return_none_for_index_error
    def get_isbn13(self) -> int:
        isbn13 = re.findall(r"isbn13: [0-9]{13}", str(self.soup))
        return int(isbn13[0].split()[1])

    @return_none_for_attribute_error
    def get_year_first_published(self) -> int:
        year_first_published = self.soup.find("nobr", attrs={"class": "greyText"}).string.strip()
        return int(re.search("([0-9]{3,4})", year_first_published).group())

    @return_none_for_attribute_error
    def get_author_full_name(self):
        return self.soup.find('a', {'class': 'authorName'}).text.strip()

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
    def _get_shelves_url(self):
        shelves_url = self.soup.find("a", text="See top shelves…")["href"]
        return f"{self.GOODREADS_BASE_URL}{shelves_url}"

    @staticmethod
    @return_none_for_index_error
    def _get_unformatted_shelves(soup: bs4.BeautifulSoup) -> [str]:
        nodes = soup.find_all("div", {"class": "shelfStat"})
        return [" ".join(node.text.strip().split()) for node in nodes]

    def get_shelves(self) -> Dict:
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
    @return_none_for_index_error
    def _get_shelf_name(shelf: str) -> str:
        return shelf.split()[:-2][0]

    @staticmethod
    @return_none_for_index_error
    def _get_shelf_count(shelf: str) -> int:
        return int(shelf.split()[-2].replace(",", ""))


    def get_lists(self):

        lists = []
        list_count_dict = {}

        if self.soup.find('a', text='More lists with this book...'):

            lists_url = self.soup.find('a', text='More lists with this book...')['href']

            source = get_response('https://www.goodreads.com' + lists_url)
            soup = bs4.BeautifulSoup(source.content, 'lxml')
            lists += [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'cell'})]

            i = 0
            while soup.find('a', {'class': 'next_page'}) and i <= 10:
                time.sleep(2)
                next_url = 'https://www.goodreads.com' + soup.find('a', {'class': 'next_page'})['href']
                source = get_response(next_url)
                soup = bs4.BeautifulSoup(source.content, 'lxml')

                lists += [node.text for node in soup.find_all('div', {'class': 'cell'})]
                i += 1

            # Format lists text.
            for _list in lists:
                _list_name = _list.split()[:-2][0]
                _list_count = int(_list.split()[-2].replace(',', ''))
                list_count_dict[_list_name] = _list_count

        return list_count_dict

    def get_num_ratings(self) -> str:
        return self.soup.find("meta", {"itemprop": "reviewCount"})["content"].strip()

    def get_num_reviews(self) -> str:
        return self.soup.find("meta", {"itemprop": "reviewCount"})["content"].strip()

    def get_average_rating(self) -> str:
        return self.soup.find("span", {"itemprop": "ratingValue"}).text.strip()

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


# url_without_year = "https://www.goodreads.com/book/show/336373.Taking_the_Path_of_Zen"
# url_without_isbn = "https://www.goodreads.com/book/show/146180.The_Adventures_of_Tintin"

all_the_pretty_horses = "https://www.goodreads.com/book/show/469571.All_the_Pretty_Horses"

res = get_response(all_the_pretty_horses)
soup = get_soup(res)
book_service = BookService(soup)

# print(book.get_book_title())
# print(book.get_numeric_book_id("5907.The_Hobbit_or_There_and_Back_Again"))
# print(book.get_book_series_name())
# print(book.get_book_series_uri())
# print(book.get_isbn())
# print(book.get_isbn13())
# print(book.get_year_first_published())
# print(book_service.get_author_full_name())
# print(book.get_num_pages())
# print(book_service.get_genres())
# print(book.get_primary_genre())
# print(book_service.get_shelves())


# print(book.get_lists())
# print(book.get_num_ratings())
# print(book.get_num_reviews())
# print(book.get_average_rating())
# print(book.get_rating_distribution())