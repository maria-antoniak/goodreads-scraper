import requests
from bs4 import BeautifulSoup
import re
import math
import sqlite3
import time
import os
import pandas as pd
import argparse


class ExtractBookId:
    """
    A class for scraping book IDs,List_Name(Collection where the book is prevalent),Votes for the list,number of books in that list from Goodreads.

    Usage:
        1. Create an instance of ExtractBookId.
        2. Call the method `scrape_page()` to start scraping.
        3. If You want to convert the ids in the db to txt format run db_to_txt method

    Example:
        >>> extractor = ExtractBookId()
        >>> extractor.scrape_page()

    Note:
        Ensure that you have an active internet connection to fetch data from Goodreads.
        The data will be stored in books_id.db
    """
    def __init__(self,list_amt_to_scrape):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.all_topic_nums=list_amt_to_scrape
        self.request_delay = 10


    def _clear_console(self):
        print("Clearing console...")
        os.system('cls' if os.name == 'nt' else 'clear')  # Windows has cls and Linux/Mac has clear
        print("Console cleared.")
        
    def scrape_page(self):

        for topic_num in self.all_topic_nums:
            page_no=0
            pages=True
            first=True
            num=0
            while pages is True:
                
                print(f'url {num} starting')
                url = f'https://www.goodreads.com/list/show/{topic_num}?page={page_no}'

                start_time = time.time()
                response = requests.get(url, headers=self.headers)
                end_time = time.time()  

                response_time = end_time - start_time  
            
                # This Adjusts sleep time based on response time
                self._adjust_sleep_time(response_time)




                html_content = response.text
                soup=BeautifulSoup(html_content,'html.parser')
                # return soup

                # Use regular expression to find href links and extract book_id from them
                href_pattern = r'href=["\'](.*?)["\']'
                id_pattern = r'/(book|title)/show/(\d+)'

                href_links = re.findall(href_pattern, html_content)
                ids = [re.search(id_pattern, link).group(2) for link in href_links if re.search(id_pattern, link)]
                ids = list(set(ids))  # Remove duplicates
                # Group_ids.extend(ids)

                print(f'{len(ids)} books have been scraped from page {page_no}.')
                
                if first is True:
                    Group_Title=self._find_title(soup=soup)
                    Books,Votes=self._find_pages(soup=soup)
                    total_pages=math.ceil(Books/100)
                
                
                if total_pages==page_no:
                    pages=False
                else:
                    page_no+=1
                
                first=False
                num+=1
                results = {
                "id": ids,
                "title": Group_Title,
                "total_Books_for_title": Books,
                "total_Votes_for_title": Votes}
            
                #exporting the data into sqlite db
                self._db_export(result_instance=results)
                print("New instances appended to SQLite database")
                self._clear_console()
            
            # results = {
            #     "id": Group_ids,
            #     "title": Group_Title,
            #     "total_Books_for_title": Books,
            #     "total_votes_for_title": Votes}
            
            # #exporting the data into sqlite db
            # self._db_export(result_instance=results)
            # time.sleep(10)
            

    def _adjust_sleep_time(self, response_time):

        if response_time > 5:  # If response time is high, increase sleep time
            self.request_delay += 1
        elif response_time < 1:  # If response time is low, decrease sleep time
            self.request_delay -= 1

        # Ensure sleep time is within reasonable bounds
        self.request_delay = max(1, self.request_delay)  # Minimum sleep time of 1 second
        self.request_delay = min(30, self.request_delay)  # Maximum sleep time of 30 seconds

        time.sleep(self.request_delay)
        print(f'Sleeping for {self.request_delay} seconds')

    def db_to_txt(self):

        # Connect to the SQLite database
        conn = sqlite3.connect('books_id.db')

        # Use Pandas to read SQL query results directly into a DataFrame
        df = pd.read_sql_query("SELECT * FROM books", conn)

        # Close the connection
        conn.close()

        # Now df contains all the data from the database table
        print(df)
        ids=df['id']
        ids.to_csv('book_ids.txt', index=False, header=False)
            
    def _find_pages(self,soup):
            '''
            Extracts the number of books and number of voters from the given BeautifulSoup object representing a web page.
            Parameters:
                soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML content of the web page.

            Returns:
                tuple: A tuple containing the number of books and the number of voters extracted from the page. If the numbers cannot be extracted, the corresponding value will be None.
            Example Usage:
                # Assume 'soup' is a BeautifulSoup object representing the parsed HTML content of the web page
                number_of_books, number_of_votes = find_pages(soup)
            ''' 
            number_of_books = 0
            number_of_votes = 0
            
            try:
                stacked_div_outer = soup.find('div', class_='stacked')
                
                if stacked_div_outer:
                    stacked_div_inner = stacked_div_outer.find('div')  
                    if stacked_div_inner:
                        div_text = stacked_div_inner.text
                        div_text_list = [item.strip() for item in div_text.split('·') if item.strip()]

                for item in div_text_list:
                    if 'books' in item:
                        # Extract the number of books
                        try:
                            number_of_books = int(item.strip().split()[0].replace(',', ''))  # Remove commas from the number
                        except ValueError:
                            number_of_books = 0  # Set to None if conversion to int fails
                    elif 'voters' in item:
                        # Extract the number of votes
                        try:
                            number_of_votes = int(item.strip().split()[0].replace(',', ''))  # Remove commas from the number
                        except ValueError:
                            number_of_votes = 0  # Set to None if conversion to int fails

                # for item in div_text_list:
                #             if 'books' in item:
                #                 number_of_books = self._extract_number(item)
                #             elif 'voters' in item:
                #                 number_of_votes = self._extract_number(item)
                        

                return number_of_books, number_of_votes
    
            except:
                return number_of_books, number_of_votes
    

    def _extract_number(self, text):
        try:
            return int(text.strip().split()[0].replace(',', ''))
        except ValueError:
            return None

           
    def _find_title(self, soup):
        h1_tags = soup.find_all('h1')

        if not h1_tags:
            return ""

        h1_texts = [tag.text for tag in h1_tags]
        title = h1_texts[0].strip()
        return title

    def _db_export(self,result_instance):

        try:
            conn = sqlite3.connect('books_id.db')

            cursor = conn.cursor()

            # Create a table if it doesn't exist with composite primary key constraint as (ID and Title)
            cursor.execute('''CREATE TABLE IF NOT EXISTS books
                            (id INTEGER NOT NULL, title TEXT NOT NULL, total_books INTEGER, total_votes INTEGER,
                            PRIMARY KEY (id, title))''')
            rows_inserted = 0
            for i,v in enumerate(result_instance["id"]):
                book_id = v
                title = result_instance.get("title", "")  # Default to empty string if title is None
                total_books = result_instance.get("total_Books_for_title", 0)
                total_votes = result_instance.get("total_Votes_for_title", 0)

                if book_id is not None and title != "":  # Check if title is not empty
                    cursor.execute('''INSERT OR IGNORE INTO books (id, title, total_books, total_votes)
                                    VALUES (?, ?, ?, ?)''', (book_id, title, total_books, total_votes))
                    rows_inserted += cursor.rowcount
                    # print(f"Inserted id: {book_id}, title: {title} into the database.Total books {total_books} and votes {total_votes}.")

                else:
                    print(f"Skipping insertion of id: {book_id}, title: {title} due to missing data.")


            print(f"Number of rows inserted: {rows_inserted}")
            

            # for id in result_instance["id"]:
            #     cursor.execute('''INSERT INTO books (id, title, total_books, total_votes)
            #                     VALUES (?, ?, ?, ?)''', (id, result_instance["title"], result_instance["total_books"], result_instance["total_votes"]))


            # Commit the transaction
            conn.commit()

            # print("New instances appended to SQLite database")

        except sqlite3.Error as e:
            print("Error occurred:", e)


        finally:
            # Close the connection
            if conn:
                conn.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape book IDs, list names, votes, and number of books from Goodreads.")
    parser.add_argument("-c", "--custom-scrap", choices=["yes", "no"], default="no",
                        help="Whether to perform custom scraping for a specific list (default: no).")
    parser.add_argument("-id", "--list-id", type=int,
                         help="The ID of the list to scrape (required if custom-scrap is 'yes'). For more information, visit: https://www.goodreads.com/list?ref=nav_brws_lists")
    parser.add_argument("-t", "--txt-convert", choices=["yes", "no"], default="no",
                        help="Whether to convert the database to a text file (default: no).")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.custom_scrap == "yes":
        if args.list_id is None:
            print("Error: --list-id argument is required when custom-scrap is 'yes'.")
            exit(1)
        else:
            if not isinstance(args.list_id, int):
                print("Error: --list-id argument must be an integer.")
                exit(1)
            else:
                list_id = args.list_id
                print(f"Custom scraping for list ID: {list_id}")
                list_amt_to_scrape = [list_id]
                
    else:
        random_scrape = 50
        list_amt_to_scrape = [i for i in range(1, random_scrape)]
    
    scrape = ExtractBookId(list_amt_to_scrape)
    scrape.scrape_page()

    if args.txt_convert == "yes":
        if os.path.exists('books_id.db'):
            print("Converting database to text file...")
            scrape.db_to_txt()
            print("Conversion completed successfully.")
        else:
            print("Error: Database file 'books_id.db' not found.")
            exit(1)


if __name__ == "__main__":
    main()