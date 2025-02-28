from database_operations import create_database, insert_review
import argparse
from datetime import datetime
import os
import re
import time
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from langdetect import detect
import requests
import logging
import sqlite3


start_time = datetime.now()
script_name = os.path.basename(__file__)



def is_english(text):
        try:
            return detect(text) == 'en'
        except:
            return False
        
def get_user_id(article):

    avatar=article.find('section',class_='ReviewerProfile__avatar')
    user_id_link=avatar.a['href']
    user_id = re.search(r'\d+', user_id_link).group()
    return user_id

def get_rating_and_date_user(article):
    rating_date_user = article.find('section', class_='ReviewCard__row')
    date_element = rating_date_user.find('span', class_='Text__body3').find('a')
    review_date = date_element.get_text(strip=True) if date_element else None

    rating_element = rating_date_user.find('span', class_='RatingStars__small')
    aria_label = rating_element['aria-label'] if rating_element else None
    if aria_label:
        rating = aria_label 
    else:
        rating = None
    return review_date,rating

def get_reviewers_info(review_articles,book_id):
    english_reviews_info = []

    for i,article in enumerate(review_articles):
        if i==5:# only first 5 reviews
            break
        # Extract review content
        review_content = article.find(class_='TruncatedContent__text').get_text(strip=True)#working
        
        if is_english(review_content):

            try:
                # Extract reviewer name
                reviewer_name = article.find(class_='ReviewerProfile__name').get_text(strip=True)
            except AttributeError:
                reviewer_name = None  

            try:
                # Extract reviewer ID
                reviewer_id = get_user_id(article)
            except Exception as e:
                print(f"Error extracting reviewer ID: {e}")
                reviewer_id = None  

            try:
                # Extract likes on review
                likes_on_review = article.find(class_='Button--subdued').get_text(strip=True)
            except AttributeError:
                likes_on_review = None  

            try:
                # Extract reviewer followers
                reviewer_followers = article.find(class_='ReviewerProfile__meta').find_all('span')[1].get_text(strip=True)
            except (AttributeError, IndexError):
                reviewer_followers = None  

            try:
                # Extract reviewer total reviews
                reviewer_total_reviews = article.find(class_='ReviewerProfile__meta').find_all('span')[0].get_text(strip=True)
            except (AttributeError, IndexError):
                reviewer_total_reviews = None  

            try:
                # Extract review date and rating
                review_date, review_rating = get_rating_and_date_user(article)
            except Exception as e:
                print(f"Error extracting review date and rating: {e}")
                review_date = review_rating = None  
            
              # Check if all fields are None
            if all(value is None for value in [reviewer_name, reviewer_id, likes_on_review, reviewer_followers,reviewer_total_reviews, review_date, review_rating]):
                continue

            english_reviews_info.append({
                'book_id': book_id,
                'reviewer_id': reviewer_id,
                'reviewer_name': reviewer_name,
                'likes_on_review': likes_on_review,
                'review_content': review_content,
                'reviewer_followers': reviewer_followers,
                'reviewer_total_reviews': reviewer_total_reviews,
                'review_date': review_date,
                'review_rating': review_rating
            })
    return english_reviews_info


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str)
    parser.add_argument('--output_directory_path', type=str)
    return parser.parse_args()

def scrape_book_reviews():
    args = parse_arguments()

    if not args.book_ids_path:
        raise ValueError("Please provide a file path containing Goodreads book IDs using the --book_ids_path flag.")
    # Create or connect to the database
    create_database(args.output_directory_path)

    # Read book IDs from the file
    with open(args.book_ids_path, 'r') as f:
        book_ids = [line.strip() for line in f if line.strip()]

    # Find books that have not been scraped yet
    conn = sqlite3.connect(args.output_directory_path +'/book_reviews.db')
    c = conn.cursor()
    c.execute('SELECT book_id FROM book_reviews')
    books_already_scraped = [row[0] for row in c.fetchall()]
    books_to_scrape = [book_id for book_id in book_ids if book_id not in books_already_scraped]

    

    # Set up logging
    logging.basicConfig(filename='error.log', level=logging.ERROR)

    for i, book_id in enumerate(books_to_scrape):
        retries = 3  # Number of retry attempts
        while retries > 0:
            try:
                url = 'https://www.goodreads.com/book/show/' + book_id
                response = requests.get(url)
                time.sleep(2)
                soup = BeautifulSoup(response.content, 'html.parser')

                review_articles = soup.find_all('article', class_='ReviewCard')
                results = get_reviewers_info(review_articles,book_id)
                if results:
                    print(str(datetime.now()) + ' ' + script_name + ': Scraped ✨' + str(len(results)) + '✨ reviews for ' + book_id)
                    print('=============================')

                # Insert to db
                for review_info in results:
                    insert_review(conn, review_info)
                # conn.close()
                break  # Exit the loop if successful

            except HTTPError:
                print("HTTP Error occurred. Retrying...")
                retries -= 1
                time.sleep(2)  # Wait for 2 seconds before retrying
            
            except Exception as e:
                print("An error occurred:", e)
                logging.error("An error occurred while processing book ID %s: %s", book_id, e)
                break  # Exit the loop if an error occurs (no need to retry)
        
        else:
            logging.error("Failed to fetch book reviews for book ID %s after multiple attempts.", book_id)
            print("Failed to fetch book reviews for book ID", book_id, "after multiple attempts.")
    if conn:
        conn.close()
    print(str(datetime.now()) + ' ' + script_name + f':\n\n🎉 Success! All book reviews scraped. 🎉\n\nGoodreads review files have been output to /{args.output_directory_path}\nGoodreads scraping run time = ⏰ ' + str(datetime.now() - start_time) + ' ⏰')

            
def main():

    scrape_book_reviews()

if __name__== "__main__":
    main()












   