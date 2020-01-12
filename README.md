# goodreads-scraper

You can use these scripts to scrape JSON-formatted book data and reviews from Goodreads.

If Goodreads is updated, these scripts might no longer work correctly.

## Dependencies

- Python 3
- Beautiful Soup 4
- Selenium

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

Goodreads only allows the first 10 pages (300 reviews) of reviews to be shown for each book. By default, the reviews are sorted by their popularity. They can also be sorted chronologically to show either the newest or oldest reviews.

We also select a filter to only show English language reviews. 

### Usage

`python get_reviews.py --book_ids_path your_file_path --output_directory_path your_directory_path --sort_order your_sort_order`

`sort_order` can be set to `0` (default), `1` (newest), or `2` (oldest).

## Authors

Maria Antoniak and Melanie Walsh
