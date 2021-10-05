# Goodreads Scraper

These services can be used to collect metadata, book reviews and generate ids from Goodreads.

We were motivated to develop this Goodreads Scraper because the Goodreads API is difficult to work with 
and does not provide access to the full text of reviews. 
The Goodreads Scraper instead uses the following libraries to collect data:

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) 
- [Selenium](https://selenium-python.readthedocs.io/installation.html)
 
We used this Goodreads Scraper to collect data for our article, 
"The Goodreads ‘Classics’: A Computational Study of Readers, Amazon, and Crowdsourced Literary Criticism." 
To allow others to reproduce (approximately) the data we used in the essay, we include a file 
with 144 Goodreads book IDs for the 144 classics that we analyzed (`example/data/goodreads_classics.txt`). 

You can use these book IDs to collect corresponding reviews and metadata with the Goodreads Scraper as described below.

*Note: Updates to the Goodreads website may break this code. 
We don't guarantee that the scraper will continue to work in the future, 
but feel free to post an issue if you run into a problem.*

# What You Need

To run these services, you will need [Python 3](https://www.python.org/downloads/).

You will also need the following Python libraries:

- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- [Selenium](https://selenium-python.readthedocs.io/installation.html)
- [chromedriver-py](https://pypi.org/project/chromedriver-py/)
- [geckodriver-autoinstaller](https://pypi.org/project/geckodriver-autoinstaller/)
- [lxml](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)
- [requests](https://docs.python-requests.org/en/master/index.html)

You can install these Python libraries by running `pip install -r requirements.txt`

Finally, you will need a web browser — either Chrome or Firefox. 
We have found that the Goodreads Scraper tends to function better with Firefox.

# Tests

Run tests with `pytest --cov-report term-missing --cov=src/` from the root directory.

# Tutorial

We recommend running these services from the command line, as the usage instructions below describe.  
However, we have also created a Jupyter notebook tutorial that demonstrates proper usage. 

Please note that these services may not work consistently from a Jupyter notebook environment 
and that the tutorial is mostly intended for demonstration purposes.

- [Jupyter notebook tutorial](https://github.com/maria-antoniak/goodreads-scraper/blob/master/example/How-To-Use-Goodreads-Scraper.ipynb) 

# Scraping Goodreads Book Metadata

You can use the below commands to collect metadata about books on Goodreads, 
such as the total number of Goodreads reviews and ratings, average Goodreads rating, 
and most common Goodreads "shelves" for each book. 

`python main.py --service book ---book_ids_path example/data/goodreads_classics.txt --output_directory_path . --format csv`

or

`python main.py -s book -bip example/data/goodreads_classics_sample.txt -odp . -f csv`


### Input

This service takes as input a list of book IDs, stored in a plain text file with one book ID per line. 
Book IDs are unique to Goodreads and can be found at the end of a book's URL. 
For example, the book ID for *Little Women* 
([https://www.goodreads.com/book/show/1934.Little_Women](https://www.goodreads.com/book/show/1934.Little_Women)) 
is `1934.Little_Women`. 

### Output

The service outputs a JSON file for each book with the information marked as `True` under [BOOK_DATA] in `config.ini`. 
By default, all values listed will be included in the output.

This service also outputs an aggregated JSON file with information about all the books that have been scraped. 
To output an aggregated CSV file in addition to a JSON file, use the flag `--format CSV`.

### Usage

Note: JSON is the default export format if not explicitly provided

`python main.py -s book -bip example/data/goodreads_classics_sample.txt -odp ./_output/ -f csv`

# Scraping Goodreads Book Reviews

You can use the review service to collect reviews and review metadata about books on Goodreads, 
including the text of the review, star rating, username of the reviewer, number of likes, 
and categories or "shelves" that the user has tagged for the book.

### Input

This service takes as input a list of book IDs, stored in a plain text file with one book ID per line. 

### Output

This service outputs a JSON file for each book with the following information:

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

This service also outputs an aggregated JSON file with information about all the reviews
for all the books that have been scraped.  
To output an aggregated CSV file in addition to a JSON file, use the flag `--format csv`.

Goodreads only allows the first 10 pages of reviews to be shown for each book. 
There are 30 reviews per page, so you should expect a maximum of 300 reviews per book. 
By default, the reviews are sorted by their popularity. 
They can also be sorted chronologically to show either the newest or oldest reviews.

We also select a filter to only show English language reviews. 

### Usage

`python src/review/review_service.py --book_ids_path example/data/goodreads_classics_sample.txt --output_directory_path . --browser firefox --sort_order newest --format json`

- `sort_order` can be set to `default`,`newest` or `oldest`.
- `browser` can be set to `chrome` or `firefox`. 
- `format` can be set to `JSON` (default) or `CSV`.

# Test

You can run the provided test script to check that everything is working correctly.

`sh ./example/shell/test_script.sh`

This will create a directory called `test-output` in which you'll find the scraped books and reviews.

# Scraping Goodreads Book ids

You can use the service `book_id` to collect book ids which can then be used as input to any of the above services.

### Input

This service takes as input a list of queries stored as plain text with one `book_title - book_author` per line.
The default location of this file is `user_io/input/goodreads_queries.txt`
The delimiter can be whatever you wish, but it must be specified in the config file: `config.ini` (the default is " - ") 

### Output

For matches, this script outputs a book id for each book here `user_io/output/matches/matches.txt`
For no matches, the script outputs the original query here `user_io/output/matches/no_matches.txt`

### Usage

`python main.py -s book_id`

Should you wish to change the match percentages or output paths, you can do so in the `config.ini`.

Percentages are currently set as follows:

`BOOK_TITLE_SIMILARITY_PERCENTAGE = 0.6`
`AUTHOR_NAME_SIMILARITY_PERCENTAGE = 0.7`

I found these to be sane defaults during testing, but it really will depend on your use case, feel free to experiment :)


# Glossary

- `book_id_title` corresponds to the id contained in the goodreads URL, e.g. `587393.The_Lost_Scrapbook` in `https://www.goodreads.com/book/show/587393.The_Lost_Scrapbook`
- `numeric_book_id` corresponds to the numeric section of the book_id_title, e.g. `587393` in `587393.The_Lost_Scrapbook`

# Credit

This code is written by Maria Antoniak and Melanie Walsh. The code is licensed under a [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/#).

If you use this scraper, we'd love to hear about your project and how you use the code.

We used a function written by [Omar Einea](https://github.com/OmarEinea/GoodReadsScraper), licensed under [GPL v3.0](https://github.com/OmarEinea/GoodReadsScraper/blob/master/LICENSE.md), for the Goodreads review sorting.