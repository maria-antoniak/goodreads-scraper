from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("/home/studs/PycharmProjects/goodreads-scraper/config.ini")

# BOOK

config_author_first_name = config_object["BOOK"].getboolean("AUTHOR_FIRST_NAME")
config_author_full_name = config_object["BOOK"].getboolean("AUTHOR_FULL_NAME")
config_author_last_name = config_object["BOOK"].getboolean("AUTHOR_LAST_NAME")
config_average_rating = config_object["BOOK"].getboolean("AVERAGE_RATING")
config_century_of_publication = config_object["BOOK"].getboolean(
    "CENTURY_OF_PUBLICATION"
)
config_genres = config_object["BOOK"].getboolean("GENRES")
config_isbn = config_object["BOOK"].getboolean("ISBN")
config_isbn13 = config_object["BOOK"].getboolean("ISBN13")
config_lists = config_object["BOOK"].getboolean("LISTS")
config_lists_url = config_object["BOOK"].getboolean("LISTS_URL")
config_number_of_pages = config_object["BOOK"].getboolean("NUMBER_OF_PAGES")
config_number_of_ratings = config_object["BOOK"].getboolean("NUMBER_OF_RATINGS")
config_number_of_reviews = config_object["BOOK"].getboolean("NUMBER_OF_REVIEWS")
config_numeric_id = config_object["BOOK"].getboolean("NUMERIC_ID")
config_primary_genre = config_object["BOOK"].getboolean("PRIMARY_GENRE")
config_rating_distribution = config_object["BOOK"].getboolean("RATING_DISTRIBUTION")
config_series_name = config_object["BOOK"].getboolean("SERIES_NAME")
config_series_url = config_object["BOOK"].getboolean("SERIES_URL")
config_shelves = config_object["BOOK"].getboolean("SHELVES")
config_title = config_object["BOOK"].getboolean("TITLE")
config_title_id = config_object["BOOK"].getboolean("TITLE_ID")
config_year_of_publication = config_object["BOOK"].getboolean("YEAR_OF_PUBLICATION")
