# Goodreads Scraper

These Python scripts can be used to collect book reviews and metadata from Goodreads.

We were motivated to develop this Goodreads Scraper because the Goodreads API is difficult to work with and does not provide access to the full text of reviews. The Goodreads Scraper instead uses the web scraping libraries [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) and [Selenium](https://selenium-python.readthedocs.io/installation.html) to collect data.

We used this Goodreads Scraper to collect data for our article, "The Goodreads ‘Classics’: A Computational Study of Readers, Amazon, and Crowdsourced Literary Criticism." To allow others to reproduce (approximately) the data we used in the essay, we include a file with 144 Goodreads book IDs for the 144 classics that we analyzed (`goodreads_classics.txt`). You can use these IDs to collect corresponding reviews and metadata with the Goodreads Scraper as described below.

*Note: Updates to the Goodreads website may break this code. We don't guarantee that the scraper will continue to work in the future, but feel free to post an issue if you run into a problem.*

<br><br>

# What You Need

To run these scripts, you will need [Python 3](https://www.anaconda.com/distribution/).

You will also need the following Python libraries:
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- [Selenium](https://selenium-python.readthedocs.io/installation.html)
- [lxml](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)
- [geckodriver-autoinstaller](https://pypi.org/project/geckodriver-autoinstaller/)
- [chromedriver-py](https://pypi.org/project/chromedriver-py/)
- [requests](https://docs.python-requests.org/en/master/index.html)

You can install these Python libraries by running `pip install -r requirements.txt`

Finally, you will need a web browser — either Chrome or Firefox. We have found that the Goodreads Scraper tends to function better with Firefox.

<br><br>

# Tutorial

We recommend running these Python scripts from the command line, as the usage instructions below describe. However, we have also created a [Jupyter notebook tutorial](https://github.com/maria-antoniak/goodreads-scraper/blob/master/How-To-Use-Goodreads-Scraper.ipynb) that demonstrates how to use the Goodreads Scraper scripts. Please note that these scripts may not work consistently from a Jupyter notebook environment and that the tutorial is mostly intended for demonstration purposes.
<br><br>

# Scraping Goodreads Book Metadata

You can use the Python script `get_books.py` to collect metadata about books on Goodreads, such as the total number of Goodreads reviews and ratings, average Goodreads rating, and most common Goodreads "shelves" for each book. 

## get_books.py

### Input

This script takes as input a list of book IDs, stored in a plain text file with one book ID per line. Book IDs are unique to Goodreads and can be found at the end of a book's URL. For example, the book ID for *Little Women* ([https://www.goodreads.com/book/show/1934.Little_Women](https://www.goodreads.com/book/show/1934.Little_Women)) is `1934.Little_Women`. 

### Output

This script outputs a JSON file for each book with the following information:

- book ID and title
- book ID 
- book title
- ISBN
- ISBN13
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

This script also outputs an aggregated JSON file with information about all the books that have been scraped. To output an aggregated CSV file in addition to a JSON file, use the flag `--format CSV`.

### Usage

`python get_books.py --book_ids_path your_file_path --output_directory_path your_directory_path --format JSON (default) or CSV`

### Example

`python get_books.py --book_ids_path most_popular_classics.txt --output_directory_path goodreads_project/classic_book_metadata --format CSV`

<br><br>

# Scraping Goodreads Book Reviews

You can use the Python script `get_reviews.py` to collect reviews and review metadata about books on Goodreads, including the text of the review, star rating, username of the reviewer, number of likes, and categories or "shelves" that the user has tagged for the book.

## get_reviews.py

### Input

This script takes as input a list of book IDs, stored in a plain text file with one book ID per line. Book IDs are unique to Goodreads and can be found at the end of a book's URL. For example, the book ID for *Little Women* ([https://www.goodreads.com/book/show/1934.Little_Women](https://www.goodreads.com/book/show/1934.Little_Women)) is `1934.Little_Women`. 

### Output

This script outputs a JSON file for each book with the following information:
- book ID and title
- book ID
- book title
- review URL
- review ID
- date
- rating
- username of the reviewer
- text
- number of likes the review received from other users
- shelves to which the reviewer added the book

This script also outputs an aggregated JSON file with information about all the reviews for all the books that have been scraped.  To output an aggregated CSV file in addition to a JSON file, use the flag `--format CSV`.

Goodreads only allows the first 10 pages of reviews to be shown for each book. There are 30 reviews per page, so you should expect a maximum of 300 reviews per book. By default, the reviews are sorted by their popularity. They can also be sorted chronologically to show either the newest or oldest reviews.

We also select a filter to only show English language reviews. 

### Usage

`python get_reviews.py --book_ids_path your_file_path --output_directory_path your_directory_path --browser your_browser_name --sort_order your_sort_order  --format JSON (default) or CSV`

`sort_order` can be set to `default`,`newest` or `oldest`.

`browser` can be set to `chrome` or `firefox`. 

`format` can be set to `JSON` (default) or `CSV`.

### Example

`python get_reviews.py --book_ids_path most_popular_classics.txt --output_directory_path goodreads_project/classic_book_reviews --sort_order default --browser chrome`

<br><br>

# Test

You can run the provided test script to check that everything is working correctly.

`./test_scripts.sh`

This will create a directory called `test-output` in which you'll find the scraped books and reviews.

<br><br>

# Scraping Goodreads Book ids

You can use the Python script `get_book_ids.py` to collect book ids which can then be used as input to any of the above scripts.

### Input

This script takes as input a list of queries (the default location is here `get_book_ids/input/goodreads_queries.txt`), stored as plain text with one `book_title - book_author` per line. The delimiter can be whatever you wish, but it must be specified in the config file here: `config.ini` (the default is " - ") 

### Output

For matches, this script outputs a book id for each book here `get_book_ids/output/matches/matches.txt`
For no matches, the script outputs the original query here `get_book_ids/output/no_matches/no_matches.txt`

### Usage

`python get_book_ids.py`

Should you wish to change the match percentages, you can do so in the `config.ini`.

Percentages are currently set as follows:

`BOOK_TITLE_SIMILARITY_PERCENTAGE = 0.6`
`AUTHOR_NAME_SIMILARITY_PERCENTAGE = 0.7`

I found these to be sane defaults during testing, but it really will depend on your use case, feel free to experiment :)

# Test

Run tests with `pytest` from the root directory.

# Credit

This code is written by Maria Antoniak and Melanie Walsh. The code is licensed under a [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/#).

If you use this scraper, we'd love to hear about your project and how you use the code.

We used a function written by [Omar Einea](https://github.com/OmarEinea/GoodReadsScraper), licensed under [GPL v3.0](https://github.com/OmarEinea/GoodReadsScraper/blob/master/LICENSE.md), for the Goodreads review sorting.

