# define methods to operate on data

import re
from common.data_access.get_book import get_response, get_soup
import bs4
from requests.models import Response
from typing import Union

from typing import Dict
import time


class GetBookService:
    def __init__(self, soup: bs4.BeautifulSoup):

        self.soup = soup

    @staticmethod
    def get_numeric_book_id(book_id_title: str) -> str:
        return book_id_title.split(".")[0]

    def get_book_title(self) -> str:
        return self.soup.find(id="bookTitle").find("h1").strip()

    def get_book_series(self) -> str:
        return self.soup.find(id="bookSeries").find("a").text.strip()

    def get_book_series_uri(self) -> str:
        BASE_URL = "https://www.goodreads.com"
        uri = self.soup.find(id="bookSeries").find("a")['href']
        return f"{BASE_URL}{uri}"

    def get_isbn(self) -> str:
        isbn = re.findall(r"nisbn: [0-9]{10}", str(self.soup))

        try:
            return isbn[0].split()[1]
        except IndexError:
            return ""

    def get_isbn13(self) -> str:
        isbn13 = re.findall(r"nisbn13: [0-9]{13}", str(self.soup))

        try:
            return isbn13[0].split()[1]
        except IndexError:
            return ""

    def get_year_first_published(self) -> str:
        try:
            year_first_published = self.soup.find("nobr", attrs={"class": "greyText"}).string.strip()
            return re.search("([0-9]{3,4})", year_first_published).group()
        except AttributeError:
            return ""

    def get_author(self) -> str:
        return self.soup.find('span', {'itemprop': 'name'}).text.split()

    def get_num_pages(self) -> int:
        if self.soup.find("span", {"itemprop": "numberOfPages"}):
            num_pages = soup.find("span", {"itemprop": "numberOfPages"}).text.strip()
            return int(num_pages.split()[0])
        return ""

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

    def get_primary_genre(self) -> str:
        return "".join(GetBookService.get_genres(self)[0])

    def get_shelves(self) -> Dict:
        shelf_count_dict = {}

        if self.soup.find("a", text="See top shelves…"):

            # Find shelves text.
            shelves_url = self.soup.find("a", text="See top shelves…")["href"]
            source = get_response("https://www.goodreads.com" + shelves_url)
            soup = bs4.BeautifulSoup(source.content, "lxml")
            shelves = [
                " ".join(node.text.strip().split())
                for node in soup.find_all("div", {"class": "shelfStat"})
            ]

            # Format shelves text.
            shelf_count_dict = {}
            for _shelf in shelves:
                _shelf_name = _shelf.split()[:-2][0]
                _shelf_count = int(_shelf.split()[-2].replace(",", ""))
                shelf_count_dict[_shelf_name] = _shelf_count

        return shelf_count_dict

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

url_without_year = "https://www.goodreads.com/book/show/336373.Taking_the_Path_of_Zen"
url_without_isbn = "https://www.goodreads.com/book/show/146180.The_Adventures_of_Tintin"
url_with_isbn = "https://www.goodreads.com/book/show/5907.The_Hobbit_or_There_and_Back_Again"
res = get_response(url_without_isbn)
soup = get_soup(res)

get_books = GetBookService(soup)

# print(get_books.get_book_title())
# print(get_books.get_numeric_book_id())
# print(get_books.get_book_title())
# print(get_books.get_book_series())
# print(get_books.get_book_series_uri())
# print(get_books.get_isbn())
# print(get_books.get_isbn13())
print(get_books.get_year_first_published())
# print(get_books.get_author())
# print(get_books.get_num_pages())
# print(get_books.get_genres())
# print(get_books.get_primary_genre())
# print(get_books.get_shelves())
# print(get_books.get_lists())
# print(get_books.get_num_ratings())
# print(get_books.get_num_reviews())
# print(get_books.get_average_rating())
# print(get_books.get_rating_distribution())