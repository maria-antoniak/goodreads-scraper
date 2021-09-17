# define methods to operate on data

import re
from common.data_access.get_book import get, parse_book
import bs4

from typing import Dict
import time


class GetBookService:
    def __init__(self, soup):

        self.soup = soup

    def get_book_id_title(self) -> str:
        return self.soup.find("a", {"class": "inter uitext greyText right"})[
            "href"
        ].replace("/book/edit/", "")

    def get_numeric_book_id(self) -> str:
        pattern = re.compile("([^.-]+)")
        book_id_title = GetBookService.get_book_id_title(self)
        return pattern.search(book_id_title).group()

    def get_book_title(self) -> str:
        return self.soup.find("h1", {"id": "bookTitle"}).text.strip()

    def get_book_series(self) -> str:
        series = self.soup.find(id="bookSeries").find("a")
        if series:
            series_name = re.search(r"\((.*?)\)", series.text).group(1)
            return series_name
        return ""

    def get_book_series_uri(self) -> str:
        series = self.soup.find(id="bookSeries").find("a")
        if series:
            series_uri = series.get("href")
            return series_uri
        return ""

    def get_isbn(self) -> str:
        try:
            isbn = re.findall(r"nisbn: [0-9]{10}", str(self.soup))[0].split()[1]
            return isbn
        except:
            return "isbn not found"

    def get_isbn13(self) -> str:
        try:
            isbn13 = re.findall(r"nisbn13: [0-9]{13}", str(self.soup))[0].split()[1]
            return isbn13
        except:
            return "isbn13 not found"

    def get_year_first_published(self) -> str:
        year_first_published = self.soup.find("nobr", attrs={"class": "greyText"})
        if year_first_published:
            year_first_published = year_first_published.string
            return re.search("([0-9]{3,4})", year_first_published).group(1)
        else:
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
            source = get("https://www.goodreads.com" + shelves_url)
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

            source = get('https://www.goodreads.com' + lists_url)
            soup = bs4.BeautifulSoup(source.content, 'lxml')
            lists += [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'cell'})]

            i = 0
            while soup.find('a', {'class': 'next_page'}) and i <= 10:
                time.sleep(2)
                next_url = 'https://www.goodreads.com' + soup.find('a', {'class': 'next_page'})['href']
                source = get(next_url)
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


soup = parse_book("636223.Ice")

get_books = GetBookService(soup)

print(get_books.get_book_title())
print(get_books.get_numeric_book_id())
print(get_books.get_book_title())
print(get_books.get_book_series())
print(get_books.get_book_series_uri())
print(get_books.get_isbn())
print(get_books.get_isbn13())
print(get_books.get_year_first_published())
print(get_books.get_author())
print(get_books.get_num_pages())
print(get_books.get_genres())
print(get_books.get_primary_genre())
print(get_books.get_shelves())
print(get_books.get_lists())
print(get_books.get_num_ratings())
print(get_books.get_num_reviews())
print(get_books.get_average_rating())
print(get_books.get_rating_distribution())