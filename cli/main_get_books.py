import argparse
from datetime import datetime
from typing import AnyStr
import json
import os
import re
import time

from urllib.request import urlopen
from urllib.error import HTTPError
from get_web_driver import get_web_driver
import bs4
import pandas as pd
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By

from dataclasses import dataclass


def get_all_lists(soup):
    lists = []
    list_count_dict = {}

    if soup.find('a', text='More lists with this book...'):

        lists_url = soup.find('a', text='More lists with this book...')['href']

        source = urlopen('https://www.goodreads.com' + lists_url)
        soup = bs4.BeautifulSoup(source, 'lxml')
        lists += [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'cell'})]

        i = 0
        while soup.find('a', {'class': 'next_page'}) and i <= 10:
            time.sleep(2)
            next_url = 'https://www.goodreads.com' + soup.find('a', {'class': 'next_page'})['href']
            source = urlopen(next_url)
            soup = bs4.BeautifulSoup(source, 'lxml')

            lists += [node.text for node in soup.find_all('div', {'class': 'cell'})]
            i += 1

        # Format lists text.
        for _list in lists:
            # _list_name = ' '.join(_list.split()[:-8])
            # _list_rank = int(_list.split()[-8][:-2]) 
            # _num_books_on_list = int(_list.split()[-5].replace(',', ''))
            # list_count_dict[_list_name] = _list_rank / float(_num_books_on_list)     # TODO: switch this back to raw counts
            _list_name = _list.split()[:-2][0]
            _list_count = int(_list.split()[-2].replace(',', ''))
            list_count_dict[_list_name] = _list_count

    return list_count_dict


def get_shelves(soup):
    shelf_count_dict = {}

    if soup.find('a', text='See top shelves…'):

        # Find shelves text.
        shelves_url = soup.find('a', text='See top shelves…')['href']
        source = urlopen('https://www.goodreads.com' + shelves_url)
        soup = bs4.BeautifulSoup(source, 'lxml')
        shelves = [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'shelfStat'})]

        # Format shelves text.
        shelf_count_dict = {}
        for _shelf in shelves:
            _shelf_name = _shelf.split()[:-2][0]
            _shelf_count = int(_shelf.split()[-2].replace(',', ''))
            shelf_count_dict[_shelf_name] = _shelf_count

    return shelf_count_dict


def get_genres(soup):
    genres = []
    for node in soup.find_all('div', {'class': 'left'}):
        current_genres = node.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
        current_genre = ' > '.join([g.text for g in current_genres])
        if current_genre.strip():
            genres.append(current_genre)
    return genres


def get_series_name(soup, driver):
    series = soup.find(id="bookSeries").find("a")
    if not series:
        return ""
    # TODO: page has changed this will no longer work
    series_name = re.search(r'\((.*?)\)', series.text).group(1)
    return series_name


def get_series_uri(soup, driver):
    series = soup.find(id="bookSeries").find("a")
    if not series:
        return ""
    series_uri = series.get("href")
    return series_uri


def get_top_5_other_editions(soup):
    other_editions = []
    for div in soup.findAll('div', {'class': 'otherEdition'}):
        other_editions.append(div.find('a')['href'])
    return other_editions


def get_isbn(soup, driver) -> str | None:
    # try:
    #     isbn = re.findall(r'nisbn: [0-9]{10}', str(soup))[0].split()[1]
    #     return isbn
    # except:
    #     raise RuntimeError("isbn not found")
    return None


def get_isbn13(soup, driver) -> str | None:
    # try:
    #     isbn13 = re.findall(r'nisbn13: [0-9]{13}', str(soup))[0].split()[1]
    #     return isbn13
    # except:
    #     return "isbn13 not found"
    return None


def get_rating_distribution(soup):
    distribution = re.findall(r'renderRatingGraph\([\s]*\[[0-9,\s]+', str(soup))[0]
    distribution = ' '.join(distribution.split())
    distribution = [int(c.strip()) for c in distribution.split('[')[1].split(',')]
    distribution_dict = {'5 Stars': distribution[0],
                         '4 Stars': distribution[1],
                         '3 Stars': distribution[2],
                         '2 Stars': distribution[3],
                         '1 Star': distribution[4]}
    return distribution_dict


def get_num_pages(soup):
    if soup.find('span', {'itemprop': 'numberOfPages'}):
        num_pages = soup.find('span', {'itemprop': 'numberOfPages'}).text.strip()
        return int(num_pages.split()[0])
    return ''


def get_year_first_published(soup):
    year_first_published = soup.find('nobr', attrs={'class': 'greyText'})
    if year_first_published:
        year_first_published = year_first_published.string
        return re.search('([0-9]{3,4})', year_first_published).group(1)
    else:
        return ''


BOOK_ID_PATTERN = re.compile("([^.-]+)")


def get_id_group(book_id: str) -> AnyStr:
    return BOOK_ID_PATTERN.search(book_id).group()


def get_cover_image_uri(driver: ChromiumDriver) -> str | None:
    el = driver.find_element(By.CSS_SELECTOR, "img[class='ResponsiveImage']")
    src = el.get_attribute('src') if el is not None else None

    return src


def get_book_title(driver: ChromiumDriver) -> str:
    el = driver.find_element(By.CSS_SELECTOR, "h1[data-testid='bookTitle']")
    title = el.text if el is not None else None

    return title


def scrape_book(book_id: str, driver: ChromiumDriver):
    url = f'https://www.goodreads.com/book/show/{book_id}'

    driver.get(url)
    source = urlopen(url)
    soup = bs4.BeautifulSoup(source, 'html.parser')

    time.sleep(2)

    book_id_title = book_id
    book_id_group = get_id_group(book_id)
    cover_image_uri = get_cover_image_uri(driver)
    book_title = get_book_title(driver)

    return {'book_id_title': book_id_title,
            'book_id': book_id_group,
            'cover_image_uri': cover_image_uri,
            'book_title': book_title,
            "book_series": get_series_name(soup, driver),
            "book_series_uri": get_series_uri(soup, driver),
            'top_5_other_editions': get_top_5_other_editions(soup),
            'isbn': get_isbn(soup, driver),
            'isbn13': get_isbn13(soup, driver),
            'year_first_published': get_year_first_published(soup),
            'authorlink': soup.find('a', {'class': 'authorName'})['href'],
            'author': ' '.join(soup.find('span', {'itemprop': 'name'}).text.split()),
            'num_pages': get_num_pages(soup),
            'genres': get_genres(soup),
            'shelves': get_shelves(soup),
            'lists': get_all_lists(soup),
            'num_ratings': soup.find('meta', {'itemprop': 'ratingCount'})['content'].strip(),
            'num_reviews': soup.find('meta', {'itemprop': 'reviewCount'})['content'].strip(),
            'average_rating': soup.find('span', {'itemprop': 'ratingValue'}).text.strip(),
            'rating_distribution': get_rating_distribution(soup)}


def condense_books(books_directory_path):
    books = []

    # Look for all the files in the directory and if they contain "book-metadata," then load them all and condense them into a single file
    for file_name in os.listdir(books_directory_path):
        if file_name.endswith('.json') and not file_name.startswith(
                '.') and file_name != "all_books.json" and "book-metadata" in file_name:
            _book = json.load(
                open(books_directory_path + '/' + file_name, 'r'))  # , encoding='utf-8', errors='ignore'))
            books.append(_book)

    return books


def get_arg_parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str)
    parser.add_argument('--output_directory_path', type=str)
    parser.add_argument('--format', type=str, action="store", default="json",
                        dest="format", choices=["json", "csv"],
                        help="set file output format")

    return parser


@dataclass
class BooksToScrape:
    books_to_scrape: list[str]
    books_already_scraped: list[str]
    book_ids: list[str]


def get_books_to_scrape(book_ids_path: str, output_directory: str) -> BooksToScrape:
    # TODO: seems this could be done easier with sets!
    with open(book_ids_path, 'r') as book_ids_file:
        book_ids = [line.strip() for line in book_ids_file if line.strip()]
    books_already_scraped = [file_name.replace('_book-metadata.json', '') for file_name in
                             os.listdir(output_directory) if
                             file_name.endswith('.json') and not file_name.startswith('all_books')]
    books_to_scrape = [book_id for book_id in book_ids if book_id not in books_already_scraped]

    return BooksToScrape(books_to_scrape=books_to_scrape, books_already_scraped=books_already_scraped, book_ids=book_ids)


def main():
    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = get_arg_parse()
    args = parser.parse_args()

    # TODO: make browser name an arg
    driver = get_web_driver('edge')

    output_directory_path = args.output_directory_path
    book_ids_path = args.book_ids_path

    scrape_info = get_books_to_scrape(book_ids_path, output_directory_path)

    condensed_books_path = f'{output_directory_path}/all_books'

    for i, book_id in enumerate(scrape_info.books_to_scrape):
        try:
            print(str(datetime.now()) + ' ' + script_name + ': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' + script_name + ': #' + str(
                i + 1 + len(scrape_info.books_already_scraped)) + ' out of ' + str(len(scrape_info.book_ids)) + ' books')

            book = scrape_book(book_id, driver)
            # Add book metadata to file name to be more specific
            json.dump(book, open(args.output_directory_path + '/' + book_id + '_book-metadata.json', 'w'))

            print('=============================')

        except HTTPError as e:
            print(e)
            exit(0)

    books = condense_books(args.output_directory_path)
    if args.format == 'json':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'), indent=4)
    elif args.format == 'csv':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'), indent=4)
        book_df = pd.read_json(f"{condensed_books_path}.json")
        book_df.to_csv(f"{condensed_books_path}.csv", index=False, encoding='utf-8')

    print(
        str(datetime.now()) + ' ' + script_name + f':\n\n🎉 Success! All book metadata scraped. 🎉\n\nMetadata files have been output to /{args.output_directory_path}\nGoodreads scraping run time = ⏰ ' + str(
            datetime.now() - start_time) + ' ⏰')


if __name__ == '__main__':
    main()
