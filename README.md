# goodreads-scraper

You can use these scripts to scrape JSON-formatted book data and reviews from Goodreads.

Updates to the Goodreads website can break this code. We don't guarantee that the scraper will continue to work in the future.

<br>

## Dependencies

- Python 3
- Beautiful Soup 4
- Selenium
- Firefox or Chrome

<br>

## Test

You can run the provided test script to check that everything is working correctly.

`./test_scripts.sh`

This will create a directory called `test-output` in which you'll find the scraped books and reviews.

<br>

## get_books.py

### Input

This script takes as input a list of book IDs, stored in a file with one bok ID per line. Book IDs are unique to Goodreads and can be found at the end of a book's URL. For example, the book ID for *Little Women* is `1934.Little_Women`. 

### Output

This script scrapes the following information for each book.
- book ID
- ISBN
- year the book was first published
- title
- author
- number of pages in the book
- genres
- top shelves
- lists
- total number of ratings
- total number of reviews
- average rating
- rating distribution

### Usage

`python get_books.py --book_ids_path your_file_path --output_directory_path your_directory_path`

<br>

## get_reviews.py

### Input

This script takes as input a list of book IDs, stored in a file with one bok ID per line. Book IDs are unique to Goodreads and can be found at the end of a book's URL. For example, the book ID for *Little Women* is `1934.Little_Women`. 

### Output

This script scrapes the following information for each review for each book.
- book ID
- review URL
- review ID
- date
- rating
- username of the reviewer
- text
- number of likes the review received from other users
- shelves to which the reviewer added the book

Goodreads only allows the first 10 pages of reviews to be shown for each book. There are 30 reviews per page, so you should expect a maximum of 300 reviews per book. By default, the reviews are sorted by their popularity. They can also be sorted chronologically to show either the newest or oldest reviews.

We also select a filter to only show English language reviews. 

### Usage

`python get_reviews.py --book_ids_path your_file_path --output_directory_path your_directory_path --browser your_browser_name --sort_order your_sort_order`

`sort_order` can be set to `0` (default), `1` (newest), or `2` (oldest).

`browser` can be set to `chrome` or `firefox`. 

<br>

## Credit

Code written by Maria Antoniak and Melanie Walsh.

We used a function written by [Omar Einea](https://github.com/OmarEinea/GoodReadsScraper) for the review sorting.

If you use this scraper, we'd love to hear about your project and how you use this code.

This is an open source tool licensed under GPL v3.0. A copy of the license can be found [here](https://github.com/OmarEinea/GoodReadsScraper/blob/master/LICENSE.md).
