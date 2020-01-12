import argparse
from datetime import datetime
import json
import os
import re
import time

from urllib.request import urlopen
from urllib.request import HTTPError
import bs4


def get_all_lists(soup):

    lists = []

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

    return lists


def get_shelves(soup):
    time.sleep(2)
    if soup.find('a', text='See top shelves…'):
        shelves_url = soup.find('a', text='See top shelves…')['href']
        source = urlopen('https://www.goodreads.com' + shelves_url)
        soup = bs4.BeautifulSoup(source, 'lxml')
        return [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'shelfStat'})]
    return ''


def get_genres(soup):
    genres = []
    for node in soup.find_all('div', {'class': 'left'}):
        current_genres = node.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
        current_genre = ' > '.join([g.text for g in current_genres])
        if current_genre.strip():
            genres.append(current_genre)
    return genres


def get_isbn(soup):
    isbn = ''
    isbn_node = soup.find('div', {'class': 'infoBoxRowTitle'}, text='ISBN')
    if not isbn_node:
        isbn_node = soup.find('div', {'class': 'infoBoxRowTitle'}, text='ISBN13')
    if isbn_node:
        isbn = ' '.join(isbn_node.find_next_sibling().text.strip().split())
    return isbn


def get_rating_distribution(soup):
    distribution = re.findall(r'renderRatingGraph\([\s]*\[[0-9,\s]+', str(soup))[0]
    distribution = ' '.join(distribution.split())
    return distribution


def get_num_pages(soup):
    if soup.find('span', {'itemprop': 'numberOfPages'}):
        return soup.find('span', {'itemprop': 'numberOfPages'}).text.strip()
    return ''


def get_year_first_published(soup):
    year_first_published = soup.find('nobr', attrs={'class':'greyText'}).string
    return re.search('([0-9]{3,4})', year_first_published).group(1)


def scrape_book(book_id):
    url = 'https://www.goodreads.com/book/show/' + book_id
    source = urlopen(url)
    soup = bs4.BeautifulSoup(source, 'html.parser')

    time.sleep(2)

    return {'book_id':              book_id, 
            'isbn':                 get_isbn(soup), 
            'year_first_published': get_year_first_published(soup), 
            'title':                soup.find('h1', {'id': 'bookTitle'}).text.strip(), 
            'author':               soup.find('span', {'itemprop': 'name'}).text.strip(), 
            'num_pages':            get_num_pages(soup), 
            'genres':               get_genres(soup), 
            'shelves':              get_shelves(soup), 
            'lists':                get_all_lists(soup), 
            'num_ratings':          soup.find('meta', {'itemprop': 'ratingCount'})['content'].strip(), 
            'num_reviews':          soup.find('meta', {'itemprop': 'reviewCount'})['content'].strip(),
            'average_rating':       soup.find('span', {'itemprop': 'ratingValue'}).text.strip(), 
            'rating_distribution':  get_rating_distribution(soup)}


def main():

    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str)
    parser.add_argument('--output_directory_path', type=str)
    args = parser.parse_args()

    book_ids              = [line.strip() for line in open(args.book_ids_path, 'rb') if line.strip()]
    books_already_scraped = [file_name.replace('.json', '') for file_name in os.listdir(args.output_directory_path)]
    books_to_scrape       = [book_id for book_id in book_ids if book_id not in books_already_scraped]

    print(str(datetime.now()) + ' ' + script_name + ': Number of books to scrape ' + str(len(books_to_scrape)))

    for i, book_id in enumerate(books_to_scrape):
        try:
            print(str(datetime.now()) + ' ' + script_name + ': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' + script_name + ': #' + str(i+1) + ' out of ' + str(len(book_ids)) + ' books')

            book = scrape_book(book_id)
            json.dump(book, open(args.output_directory_path + '/' + book_id + '.json', 'w'))

            print('=============================')

        except HTTPError as e:
            print(e)
            exit(0)

    print(str(datetime.now()) + ' ' + script_name + ': Run Time = ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    main()
