import argparse
from datetime import datetime
import json
import os
import re
import time

from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
import pandas as pd


def get_all_lists(soup):

    lists = []
    list_count_dict = {}

    if soup.find('a', string='More lists with this book...'):

        lists_url = soup.find('a', string='More lists with this book...')['href']

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
    
    if soup.find('a', string='See top shelves…'):

        # Find shelves text.
        shelves_url = soup.find('a', string='See top shelves…')['href']
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


def get_series_name(soup):
    series = soup.find(id="bookSeries")
    if not series:
        return ""
    series_link = series.find("a")
    if not series_link:
        return ""
    return re.search(r'\((.*?)\)', series_link.text).group(1)


def get_series_uri(soup):
    series = soup.find(id="bookSeries")
    if not series:
        return ""
    series_link = series.find("a")
    if not series_link:
        return ""
    return series_link.get("href")

def get_top_5_other_editions(soup):
    other_editions = []
    for div in soup.findAll('div', {'class': 'otherEdition'}):
      other_editions.append(div.find('a')['href'])
    return other_editions

def get_isbn10(soup):
    try:
        return int(re.search(r'ISBN10: *([0-9]{10})', str(soup)).group(1))
    except:
        return None

def get_isbn(soup):
    try:
        for script_tag in soup.find_all('script', {'type':'application/ld+json'}):
            data = json.loads(script_tag.string)
            if "isbn" in data:
                return data["isbn"]
        return None
    except Exception as e:
        return None

def get_rating_distribution(soup):
    histogram_div = soup.find('div', {"class": "RatingsHistogram"})
    distribution_dict = {
        '5 Stars': int(re.search(r"[0-9,]*", histogram_div.find('div', {"data-testid":"labelTotal-5"}).string).group().replace(",", "")),
        '4 Stars': int(re.search(r"[0-9,]*", histogram_div.find('div', {"data-testid":"labelTotal-4"}).string).group().replace(",", "")),
        '3 Stars': int(re.search(r"[0-9,]*", histogram_div.find('div', {"data-testid":"labelTotal-3"}).string).group().replace(",", "")),
        '2 Stars': int(re.search(r"[0-9,]*", histogram_div.find('div', {"data-testid":"labelTotal-2"}).string).group().replace(",", "")),
        '1 Stars': int(re.search(r"[0-9,]*", histogram_div.find('div', {"data-testid":"labelTotal-1"}).string).group().replace(",", "")),
    }
    return distribution_dict


def get_num_pages(soup):
    if soup.find('span', {'itemprop': 'numberOfPages'}):
        num_pages = soup.find('span', {'itemprop': 'numberOfPages'}).text.strip()
        return int(num_pages.split()[0])
    return ''


def get_year_first_published(soup):
    publication_paragraph = soup.find('p', attrs={'data-testid':'publicationInfo'})
    if publication_paragraph:
        publication_sentence = publication_paragraph.string
        return int(re.search('[0-9]{3,4}', publication_sentence).group())
    else:
        return None

def get_id(bookid):
    pattern = re.compile("([^.-]+)")
    return pattern.search(bookid).group()

def get_cover_image_uri(soup):
    series = soup.find('img', id='coverImage')
    if series:
        series_uri = series.get('src')
        return series_uri
    else:
        return ""

def get_num_ratings(soup):
    ratings_text = soup.find('span', {'data-testid': 'ratingsCount'}).text
    num_ratings = re.search(r"[0-9,]*", ratings_text).group().replace(",", "")
    return int(num_ratings)

def get_num_reviews(soup):
    reviews_text = soup.find('span', {'data-testid': 'reviewsCount'}).text
    num_reviews = re.search(r"[0-9,]*", reviews_text).group().replace(",", "")
    return int(num_reviews)

def scrape_book(book_id):
    url = 'https://www.goodreads.com/book/show/' + book_id
    source = urlopen(url)
    soup = bs4.BeautifulSoup(source, 'html.parser')

    time.sleep(2)

    return {'book_id_title':        book_id,
            'book_id':              get_id(book_id),
            'cover_image_uri':      get_cover_image_uri(soup),
            'book_title':           ' '.join(soup.find('h1', {'data-testid': 'bookTitle'}).text.split()),
            "book_series":          get_series_name(soup),
            "book_series_uri":      get_series_uri(soup),
            'top_5_other_editions': get_top_5_other_editions(soup),
            'isbn':                 get_isbn(soup),
            'isbn10':               get_isbn10(soup),
            'year_first_published': get_year_first_published(soup),
            'authorlink':           soup.find('a', {'class': 'ContributorLink'})['href'],
            'author':               soup.find('span', {'class': 'ContributorLink__name'}).string,
            'num_pages':            get_num_pages(soup),
            'genres':               get_genres(soup),
            'shelves':              get_shelves(soup),
            'lists':                get_all_lists(soup),
            'num_ratings':          get_num_ratings(soup),
            'num_reviews':          get_num_reviews(soup),
            'average_rating':       float(soup.find('div', {'class': 'RatingStatistics__rating'}).string.strip()),
            'rating_distribution':  get_rating_distribution(soup)}

def condense_books(books_directory_path):

    books = []
    
    # Look for all the files in the directory and if they contain "book-metadata," then load them all and condense them into a single file
    for file_name in os.listdir(books_directory_path):
        if file_name.endswith('.json') and not file_name.startswith('.') and file_name != "all_books.json" and "book-metadata" in file_name:
            _book = json.load(open(books_directory_path + '/' + file_name, 'r')) #, encoding='utf-8', errors='ignore'))
            books.append(_book)

    return books

def main():

    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str)
    parser.add_argument('--output_directory_path', type=str)
    parser.add_argument('--format', type=str, action="store", default="json",
                        dest="format", choices=["json", "csv"],
                        help="set file output format")
    args = parser.parse_args()

    book_ids              = [line.strip() for line in open(args.book_ids_path, 'r') if line.strip()]
    books_already_scraped =  [file_name.replace('_book-metadata.json', '') for file_name in os.listdir(args.output_directory_path) if file_name.endswith('.json') and not file_name.startswith('all_books')]
    books_to_scrape       = [book_id for book_id in book_ids if book_id not in books_already_scraped]
    condensed_books_path   = args.output_directory_path + '/all_books'

    for i, book_id in enumerate(books_to_scrape):
        try:
            print(str(datetime.now()) + ' ' + script_name + ': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' + script_name + ': #' + str(i+1+len(books_already_scraped)) + ' out of ' + str(len(book_ids)) + ' books')

            book = scrape_book(book_id)
            # Add book metadata to file name to be more specific
            json.dump(book, open(args.output_directory_path + '/' + book_id + '_book-metadata.json', 'w'), indent=4)

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
        
    print(str(datetime.now()) + ' ' + script_name + f':\n\n🎉 Success! All book metadata scraped. 🎉\n\nMetadata files have been output to /{args.output_directory_path}\nGoodreads scraping run time = ⏰ ' + str(datetime.now() - start_time) + ' ⏰')



if __name__ == '__main__':
    main()
