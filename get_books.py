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

#Doesn't Work 
# def get_all_lists(soup):

#     lists = []
#     list_count_dict = {}

#     if soup.find('a', text='More lists with this book...'):

#         lists_url = soup.find('a', text='More lists with this book...')['href']

#         source = urlopen('https://www.goodreads.com' + lists_url)
#         soup = bs4.BeautifulSoup(source, 'lxml')
#         lists += [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'cell'})]

#         i = 0
#         while soup.find('a', {'class': 'next_page'}) and i <= 10:

#             time.sleep(2)
#             next_url = 'https://www.goodreads.com' + soup.find('a', {'class': 'next_page'})['href']
#             source = urlopen(next_url)
#             soup = bs4.BeautifulSoup(source, 'lxml')

#             lists += [node.text for node in soup.find_all('div', {'class': 'cell'})]
#             i += 1

#         # Format lists text.
#         for _list in lists:
#             # _list_name = ' '.join(_list.split()[:-8])
#             # _list_rank = int(_list.split()[-8][:-2]) 
#             # _num_books_on_list = int(_list.split()[-5].replace(',', ''))
#             # list_count_dict[_list_name] = _list_rank / float(_num_books_on_list)     # TODO: switch this back to raw counts
#             _list_name = _list.split()[:-2][0]
#             _list_count = int(_list.split()[-2].replace(',', ''))
#             list_count_dict[_list_name] = _list_count

#     return list_count_dict

#Doesn't work
# def get_shelves(soup):

#     shelf_count_dict = {}
    
#     if soup.find('a', text='See top shelves…'):

#         # Find shelves text.
#         shelves_url = soup.find('a', text='See top shelves…')['href']
#         source = urlopen('https://www.goodreads.com' + shelves_url)
#         soup = bs4.BeautifulSoup(source, 'lxml')
#         shelves = [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'shelfStat'})]
        
#         # Format shelves text.
#         shelf_count_dict = {}
#         for _shelf in shelves:
#             _shelf_name = _shelf.split()[:-2][0]
#             _shelf_count = int(_shelf.split()[-2].replace(',', ''))
#             shelf_count_dict[_shelf_name] = _shelf_count

#     return shelf_count_dict


def get_genres(soup):
    genres_div = soup.find("div", {"data-testid": "genresList"})
    
    if genres_div:
        
        genre_links = genres_div.find_all("a", class_="Button--tag-inline")
        
        genres = [link.text.strip() for link in genre_links]
        
        return genres
    else:
        return []


def get_series_name(soup):
    series = soup.find(id="bookSeries").find("a")
    if series:
        series_name = re.search(r'\((.*?)\)', series.text).group(1)
        return series_name
    else:
        return ""


def get_series_uri(soup):
    series = soup.find(id="bookSeries").find("a")
    if series:
        series_uri = series.get("href")
        return series_uri
    else:
        return ""


# def get_top_5_other_editions(soup):
#     other_editions = []
#     for div in soup.findAll('div', {'class': 'otherEdition'}):
#       other_editions.append(div.find('a')['href'])
#     return other_editions


def get_publication_info(soup):
    publication_info_list = []
    a = soup.find_all('div', class_='FeaturedDetails')
    for item in a:
        publication_info = item.find('p', {'data-testid': 'publicationInfo'}).text
        publication_info_list.append(publication_info)
    return publication_info_list

def get_num_pages(soup):
    number_of_pages_list = []
    featured_details = soup.find_all('div', class_='FeaturedDetails')
    for item in featured_details:
        format_info = item.find('p', {'data-testid': 'pagesFormat'})
        if format_info:
            format_text = format_info.text
            parts = format_text.split(', ')
            if len(parts) == 2:
                number_of_pages, _ = parts
                # Extract the number from the string
                number_of_pages = ''.join(filter(str.isdigit, number_of_pages))
                number_of_pages_list.append(number_of_pages)
            elif len(parts) == 1:
                # Check if it's a number
                if parts[0].isdigit():
                    number_of_pages_list.append(parts[0])
                else:
                    number_of_pages_list.append(None)  
            else:
                number_of_pages_list.append(None) 
        else:
            number_of_pages_list.append(None)  
    return number_of_pages_list

def get_format_info(soup):
    format_info_list = []
    a = soup.find_all('div', class_='FeaturedDetails')
    for item in a:
        format_info = item.find('p', {'data-testid': 'pagesFormat'}).text
        format_info_list.append(format_info)
    return format_info_list


def get_rating_distribution(soup):
    rating_numbers = {}

    try:
        rating_bars = soup.find_all('div', class_='RatingsHistogram__bar')

        # Iterate through each rating bar
        for rating_bar in rating_bars:
            try:
                # Extract the rating (number of stars) from the aria-label attribute
                rating = rating_bar['aria-label'].split()[0]

                # Extract the number of ratings from the aria-label attribute of the labelTotal div
                label_total = rating_bar.find('div', class_='RatingsHistogram__labelTotal')
                num_ratings = label_total.get_text().split(' ')[0]

                # Store the rating number in the dictionary
                rating_numbers[rating] = num_ratings
            except (KeyError, IndexError) as e:
                print(f"Error occurred while extracting rating number for {rating}: {e}")
                # Set rating number to 0 if not found
                rating_numbers[rating] = '0'
    except AttributeError as e:
        print(f"Error occurred while finding rating bars: {e}")

    return rating_numbers


def get_cover_image_uri(soup):
    series = soup.find('img', class_='ResponsiveImage')
    if series:
        series_uri = series.get('src')
        return series_uri
    else:
        return ""
    
    
def contributor_info(soup):
    contributor = soup.find('a', {'class': 'ContributorLink'})
    return contributor  
def scrape_book(book_id):
    url = 'https://www.goodreads.com/book/show/' + book_id
    source = urlopen(url)
    soup = bs4.BeautifulSoup(source, 'html.parser')

    time.sleep(2)

    return { 'book_id':              book_id,#done
            # 'book_id':              get_id(book_id),# redundant
            'cover_image_uri':      get_cover_image_uri(soup),#done
            'book_title':           ' '.join(soup.find('h1', {'data-testid': 'bookTitle'}).text.split()),#done
            # "book_series":          get_series_name(soup),   # cannot find
            # "book_series_uri":      get_series_uri(soup),    # cannot find
            # 'top_5_other_editions': get_top_5_other_editions(soup),# inside DOM element
            # 'isbn':                 get_isbn(soup),   # inside DOM element
            # 'isbn13':               get_isbn13(soup), # inside DOM element
            'format':               get_format_info(soup),#Added
            'publication_info':     get_publication_info(soup),#Added
            'authorlink':           contributor_info(soup)['href'],#done
            'author':               contributor_info(soup).find('span', {'class': 'ContributorLink__name'}).text.strip(),#done
            'num_pages':            get_num_pages(soup),#Added/done
            'genres':               get_genres(soup),#done
            # 'shelves':              get_shelves(soup),#doesn't work
            # 'lists':                get_all_lists(soup),#doesn't work
            'num_ratings':          ''.join(filter(str.isdigit, soup.find('span', {'data-testid': 'ratingsCount'}).text)),#done
            'num_reviews':          ''.join(filter(str.isdigit, soup.find('span', {'data-testid': 'reviewsCount'}).text)),#done
            'average_rating':       soup.find('div', {'class': 'RatingStatistics__rating'}).text.strip(),#done
            'rating_distribution':  get_rating_distribution(soup)}#done

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
            json.dump(book, open(args.output_directory_path + '/' + book_id + '_book-metadata.json', 'w'))

            print('=============================')
        # This will handle if the Page doesn't exist or if there is no book title on the Goodreads website, 
        # (we get an attribute error representing there is no H1 tag on the page), Right now There are no H1 tags on the pages which dont exist.
        except AttributeError as e: 
            print(e)
            continue

        except HTTPError as e:
            print(e)
            exit(0)


    books = condense_books(args.output_directory_path)
    if args.format == 'json':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'))
    elif args.format == 'csv':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'))
        book_df = pd.read_json(f"{condensed_books_path}.json")
        book_df.to_csv(f"{condensed_books_path}.csv", index=False, encoding='utf-8')
        
    print(str(datetime.now()) + ' ' + script_name + f':\n\n🎉 Success! All book metadata scraped. 🎉\n\nMetadata files have been output to /{args.output_directory_path}\nGoodreads scraping run time = ⏰ ' + str(datetime.now() - start_time) + ' ⏰')



if __name__ == '__main__':
    main()
