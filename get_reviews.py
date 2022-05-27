import argparse
from collections import Counter
from datetime import datetime
import json
import os
import regex as re
import time
import bs4
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, ElementNotVisibleException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from urllib.request import urlopen
from urllib.error import HTTPError
from selenium.webdriver.common.by import By
import pandas as pd
import geckodriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager



RATING_STARS_DICT = {'it was amazing': 5,
                     'really liked it': 4,
                     'liked it': 3,
                     'it was ok': 2,
                     'did not like it': 1,
                     '': None}


def switch_reviews_mode(driver, book_id, sort_order, rating=None):
    """
    Copyright (C) 2019 by Omar Einea: https://github.com/OmarEinea/GoodReadsScraper
    Licensed under GPL v3.0: https://github.com/OmarEinea/GoodReadsScraper/blob/master/LICENSE.md
    Accessed on 2019-12-01.
    """
    edition_reviews=False
    rating = str(rating) if rating else ''
    driver.execute_script(
        'document.getElementById("reviews").insertAdjacentHTML("beforeend", \'<a data-remote="true" rel="nofollow"'
        f'class="actionLinkLite loadingLink" data-keep-on-success="true" id="switch{rating}{sort_order}"' +
        f'href="/book/reviews/{book_id}?rating={rating}&sort={sort_order}' +
        ('&edition_reviews=true' if edition_reviews else '') + '">Switch Mode</a>\');' +
        f'document.getElementById("switch{rating}{sort_order}").click()'
    )
    return True


def get_rating(node):
    if len(node.find_all('span', {'class': 'staticStars'})) > 0:
        rating = node.find_all('span', {'class': 'staticStars'})[0]['title']
        return RATING_STARS_DICT[rating]
    return ''


def get_user_name(node):
    if len(node.find_all('a', {'class': 'user'})) > 0:
        return node.find_all('a', {'class': 'user'})[0]['title']
    return ''

def get_user_url(node):
    if len(node.find_all('a', {'class': 'user'})) > 0:
        return node.find_all('a', {'class': 'user'})[0]['href']
    return ''


def get_date(node):
    if len(node.find_all('a', {'class': 'reviewDate createdAt right'})) > 0:
        return node.find_all('a', {'class': 'reviewDate createdAt right'})[0].text
    return ''


def get_text(node):

    display_text = ''
    full_text = ''

    if len(node.find_all('span', {'class': 'readable'})) > 0:
        for child in node.find_all('span', {'class': 'readable'})[0].children:
            if child.name == 'span' and 'style' not in child:
                display_text = child.text
            if child.name == 'span' and 'style' in child and child['style'] == 'display:none':
                full_text = child.text

    if full_text:
        return full_text

    return display_text


def get_num_likes(node):
    if node.find('span', {'class': 'likesCount'}) and len(node.find('span', {'class': 'likesCount'})) > 0:
        likes = node.find('span', {'class': 'likesCount'}).text
        if 'likes' in likes:
            return int(likes.split()[0])
    return 0


def get_shelves(node): 
    shelves = []       
    if node.find('div', {'class': 'uitext greyText bookshelves'}):
        _shelves_node = node.find('div', {'class': 'uitext greyText bookshelves'})
        for _shelf_node in _shelves_node.find_all('a'):
            shelves.append(_shelf_node.text)
    return shelves

def get_id(bookid):
    pattern = re.compile("([^.]+)")
    return pattern.search(bookid).group()

    
def scrape_reviews_on_current_page(driver, url, book_id, sort_order):

    reviews = []

    # Pull the page source, load into BeautifulSoup, and find all review nodes.
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'lxml')
    nodes = soup.find_all('div', {'class': 'review'})
    book_title = soup.find(id='bookTitle').text.strip()
    
    # Iterate through and parse the reviews.
    for node in nodes:
        review_id = re.search('[0-9]+', node['id']).group(0)
        reviews.append({'book_id_title': book_id,
                        'book_id': get_id(book_id),
                        'book_title': book_title,
                        'review_url': f"https://www.goodreads.com/review/show/{review_id}", 
                        'review_id': review_id, 
                        'date': get_date(node), 
                        'rating': get_rating(node), 
                        'user_name': get_user_name(node),
                        'user_url': get_user_url(node),
                        'text': get_text(node), 
                        'num_likes': get_num_likes(node),
                        'sort_order': sort_order,
                        'shelves': get_shelves(node)})

    return reviews


def check_for_duplicates(reviews):
    review_ids = [r['review_id'] for r in reviews]  
    num_duplicates = len([_id for _id, _count in Counter(review_ids).items() if _count > 1])
    return num_duplicates

def get_reviews_first_ten_pages(driver, book_id, sort_order, rating):

    reviews = []
    url = 'https://www.goodreads.com/book/show/' + book_id
    driver.get(url)

    source = driver.page_source

    try:
        time.sleep(4)

        # Refresh the reviews so that we account for a non-default sort order or a changed rating filter
        switch_reviews_mode(driver, book_id, sort_order, rating=rating)
        time.sleep(2)

        if sort_order == 'newest' or sort_order == 'oldest':
            select = Select(driver.find_element(By.NAME, str('language_code')))
            select.select_by_value('en')
            time.sleep(4)
    
        # Scrape the first page of reviews.
        reviews = scrape_reviews_on_current_page(driver, url, book_id, sort_order)
        print('Scraped page 1')
        # GoodReads will only load the first 10 pages of reviews.
        # Click through each of the following nine pages and scrape each page.
        page_counter = 2
        while page_counter <=10:
            try:
                if driver.find_element(By.LINK_TEXT, str(page_counter)):
                    driver.find_element(By.LINK_TEXT, str(page_counter)).click()
                    time.sleep(3)
                    reviews += scrape_reviews_on_current_page(driver, url, book_id, sort_order)
                    print(f"Scraped page {page_counter}")
                    page_counter += 1
                else:
                    return reviews
            
            except NoSuchElementException:
                if page_counter == 10:
                    try:
                        driver.find_element(By.LINK_TEXT, str(9)).click()
                        time.sleep(2)
                        continue
                    except:
                        return reviews
                else:
                    print(f'{book_id} has less than 10 pages of reviews!')
                    return reviews
            
            except ElementNotVisibleException:
                print('ERROR ElementNotVisibleException: Pop-up detected, reloading the page.')
                reviews = get_reviews_first_ten_pages(driver, book_id, sort_order, rating)
                return reviews
                        
            except ElementClickInterceptedException:
                print(f'🚨 ElementClickInterceptedException (Likely a pop-up)🚨\n🔄 Refreshing Goodreads site and skipping problem page {page_counter}🔄')
                driver.get(url)
                time.sleep(3)
                page_counter += 1
                continue
                
            except StaleElementReferenceException:
                print('ERROR: StaleElementReferenceException\nRefreshing Goodreads site and skipping problem page {page_counter} ')
                driver.get(url)
                time.sleep(3)
                page_counter += 1
                continue
                
    except ElementClickInterceptedException:
                print(f'🚨 ElementClickInterceptedException (Likely a pop-up)🚨\n🔄 Refreshing Goodreads site and rescraping book🔄')
                driver.get(url)
                time.sleep(3)
                reviews = get_reviews_first_ten_pages(driver, book_id, sort_order, rating)
                return reviews
                
    except ElementNotInteractableException:
            print('🚨 ElementNotInteractableException🚨 \n🔄 Refreshing Goodreads site and rescraping book🔄')
            reviews = get_reviews_first_ten_pages(driver, book_id, sort_order, rating)
            return reviews

        
    if check_for_duplicates(reviews) >= 30:
        print(f'ERROR: {check_for_duplicates(reviews)} duplicates found! Re-scraping this book.')
        reviews = get_reviews_first_ten_pages(driver, book_id, sort_order, rating)
        return reviews
    else:
        return reviews

    return reviews
    
def condense_reviews(reviews_directory_path):
    reviews = []
    for file_name in os.listdir(reviews_directory_path):
        # Check to see if reviews in file name
        if file_name.endswith('.json') and not file_name.startswith('.') and file_name != "all_reviews.json" and "_reviews" in file_name:
            _reviews = json.load(open(reviews_directory_path + '/' + file_name, 'r'))
            reviews += _reviews
    return reviews

def main():

    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str)
    parser.add_argument('--output_directory_path', type=str)
    parser.add_argument('--browser', type=str, help="choose a browser")
    parser.add_argument('--rating_filter', default=None, type=int)
    parser.add_argument('--sort_order', default='default', type=str)
    parser.add_argument('--format', type=str, action="store", default="json",
                        dest="format",
                        help="set file output format")
    
    args = parser.parse_args()
    
    if not args.book_ids_path:
        parser.error("\n\nPlease add the --book_ids_path flag and choose a filepath that contains Goodreads book IDs\n")
    if not args.output_directory_path:
        parser.error("\n\nPlease add the --output_directory_path and choose a directory filepath to output your reviews\n")
    if not args.browser:
        parser.error("\n\nPlease add the --browser flag and choose a browser: either Firefox or Chrome\n")

    book_ids              = [line.strip() for line in open(args.book_ids_path, 'r') if line.strip()]
    books_already_scraped = [file_name.replace('_reviews.json', '') for file_name in os.listdir(args.output_directory_path) if file_name.endswith('.json') and not file_name.startswith('all_reviews') and "_reviews" in file_name]
    books_to_scrape       = [book_id for book_id in book_ids if book_id not in books_already_scraped]
    condensed_reviews_path   = args.output_directory_path + '/all_reviews'
    
    #Set up driver
    if args.browser is not None:
        if args.browser.lower() == 'chrome':
            driver = webdriver.Chrome(ChromeDriverManager().install())
        elif args.browser.lower() == 'firefox':
            geckodriver_autoinstaller.install()
            driver = webdriver.Firefox()
       # Get an option to work with Google Colab
        elif args.browser.lower() == "colab":
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)
        else:
            print('Please select a web browser: Chrome or Firefox')
    else:
        print('Please select a web browser: Chrome or Firefox')
    
    for i, book_id in enumerate(books_to_scrape):
        try:

            print(str(datetime.now()) + ' ' + script_name + ': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' + script_name + ': #' + str(i+1+len(books_already_scraped)) + ' out of ' + str(len(book_ids)) + ' books')

            reviews = get_reviews_first_ten_pages(driver, book_id, args.sort_order, rating=args.rating_filter)

            if reviews:
                print(str(datetime.now()) + ' ' + script_name + ': Scraped ✨' + str(len(reviews)) + '✨ reviews for ' + book_id)

                if args.rating_filter:
                    filename_rating_suffix = f'_{args.rating_filter}_stars'
                else:
                    filename_rating_suffix = ''
                # add the word reviews to file name
                file_name = book_id + filename_rating_suffix + '_reviews.json'

                json.dump(reviews, open(args.output_directory_path + '/' + file_name, 'w'))

            print('=============================')

        except HTTPError:
            pass

    driver.quit()
    
    reviews = condense_reviews(args.output_directory_path)
    if args.format.lower() == 'json':
        json.dump(reviews, open(f"{condensed_reviews_path}.json", 'w'))
    elif args.format.lower() == 'csv':
        json.dump(reviews, open(f"{condensed_reviews_path}.json", 'w'))
        review_df = pd.read_json(f"{condensed_reviews_path}.json")
        review_df.to_csv(f"{condensed_reviews_path}.csv", index=False, encoding='utf-8')
    

    print(str(datetime.now()) + ' ' + script_name + f':\n\n🎉 Success! All book reviews scraped. 🎉\n\nGoodreads review files have been output to /{args.output_directory_path}\nGoodreads scraping run time = ⏰ ' + str(datetime.now() - start_time) + ' ⏰')


if __name__ == '__main__':
    main()
