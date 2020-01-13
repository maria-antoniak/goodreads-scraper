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
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
from urllib.request import urlopen
from urllib.request import HTTPError


RATING_STARS_DICT = {'it was amazing': 5,
                     'really liked it': 4,
                     'liked it': 3,
                     'it was ok': 2,
                     'did not like it': 1,
                     '': None}


def switch_reviews_mode(driver, book_id, sort_order, rating=''):
    """
    Taken from 
    """
    SORTS = ['default', 'newest', 'oldest']
    edition_reviews=False
    driver.execute_script(
        'document.getElementById("reviews").insertAdjacentHTML("beforeend", \'<a data-remote="true" rel="nofollow"'
        f'class="actionLinkLite loadingLink" data-keep-on-success="true" id="switch{rating}{sort}"' +
        f'href="/book/reviews/{book_id}?rating={rating}&sort={SORTS[sort_order]}' +
        ('&edition_reviews=true' if edition_reviews else '') + '">Switch Mode</a>\');' +
        f'document.getElementById("switch{rating}{sort}").click()'
    )
    return True


def get_rating(node):
    if len(node.find_all('span', {'class': 'staticStars'})) > 0:
        rating = node.find_all('span', {'class': 'staticStars'})[0]['title']
        return RATING_STARS_DICT[rating]
    return ''


def get_user(node):
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


def scrape_reviews_on_current_page(driver, url, book_id):

    reviews = []

    # Pull the page source, load into BeautifulSoup, and find all review nodes.
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'lxml')
    nodes = soup.find_all('div', {'class': 'review'})

    # Iterate through and parse the reviews.
    for node in nodes:
        reviews.append({'book_id': book_id, 
                        'review_url': url, 
                        'review_id': node['id'], 
                        'date': get_date(node), 
                        'rating': get_rating(node), 
                        'user': get_user(node), 
                        'text': get_text(node), 
                        'num_likes': get_num_likes(node),
                        'shelves': get_shelves(node)})

    return reviews


def check_for_duplicates(reviews):
    review_ids = [r['review_id'] for r in reviews]  
    num_duplicates = len([_id for _id, _count in Counter(review_ids).items() if _count > 1])
    if num_duplicates >= 30:
        return True
    return False


def get_reviews_first_ten_pages(driver, book_id, sort_order):

    reviews = []
    url = 'https://www.goodreads.com/book/show/' + book_id
    driver.get(url)

    source = driver.page_source

    try:

        # Re-order the reviews so that we scrape the newest or oldest reviews instead of the default.
        if sort_order != 0:
            switch_reviews_mode(driver, book_id, sort_order)
            time.sleep(2)
        
        # Filter to only English reviews (need extra step for most liked reviews).
        if sort_order == 0:
            select = Select(driver.find_element_by_name('language_code'))
            select.select_by_value('es')
            time.sleep(4)
        select = Select(driver.find_element_by_name('language_code'))
        select.select_by_value('en')
        time.sleep(4)

        # Scrape the first page of reviews.
        reviews = scrape_reviews_on_current_page(driver, url, book_id)

        # GoodReads will only load the first 10 pages of reviews.
        # Click through each of the following nine pages and scrape each page.
        for i in range(2, 11):
            try:
                if driver.find_element_by_xpath("//a[@rel='next'][text()=" + str(i) + "]"):
                    driver.find_element_by_xpath("//a[@rel='next'][text()=" + str(i) + "]").click()
                    time.sleep(2)
                    reviews += scrape_reviews_on_current_page(driver, url, book_id)
                else:
                    return reviews
            except NoSuchElementException or ElementNotInteractableException:
                print('ERROR: Could not find next page link! Re-scraping this book')
                reviews = get_reviews_first_ten_pages(driver, book_id, sort_order)
                return reviews

    except ElementClickInterceptedException:
        print('ERROR: Pop-up detected, reloading the page.')
        reviews = get_reviews_first_ten_pages(driver, book_id, sort_order)
        return reviews

    if check_for_duplicates(reviews):
        print('ERROR: Duplicates found! Re-scraping this book')
        reviews = get_reviews_first_ten_pages(driver, book_id, sort_order)
        return reviews

    return reviews


def main():

    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str)
    parser.add_argument('--output_directory_path', type=str)
    parser.add_argument('--sort_order', type=int)
    args = parser.parse_args()

    book_ids              = [line.strip() for line in open(args.book_ids_path, 'r') if line.strip()]
    books_already_scraped = [file_name.replace('.json', '') for file_name in os.listdir(args.output_directory_path)]
    books_to_scrape       = [book_id for book_id in book_ids if book_id not in books_already_scraped]

    driver = webdriver.Firefox()

    for i, book_id in enumerate(books_to_scrape):
        try:

            print(str(datetime.now()) + ' ' + script_name + ': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' + script_name + ': #' + str(i+1+len(books_already_scraped)) + ' out of ' + str(len(book_ids)) + ' books')

            reviews = get_reviews_first_ten_pages(driver, book_id, args.sort_order)

            if reviews:
                print(str(datetime.now()) + ' ' + script_name + ': Scraped ' + str(len(reviews)) + ' reviews for ' + book_id)
                json.dump(reviews, open(args.output_directory_path + '/' + book_id + '.json', 'w'))

            print('=============================')

        except HTTPError:
            pass

    driver.quit()

    print(str(datetime.now()) + ' ' + script_name + ': Run Time = ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    main()
