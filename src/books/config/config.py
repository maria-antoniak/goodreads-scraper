from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("config.ini")

# BOOK_DATA

config_book_id_title = config_object["BOOK_DATA"].getboolean("BOOK_ID_TITLE")
config_numeric_book_id = config_object["BOOK_DATA"].getboolean("NUMERIC_BOOK_ID")
config_book_title = config_object["BOOK_DATA"].getboolean("BOOK_TITLE")
config_book_series = config_object["BOOK_DATA"].getboolean("BOOK_SERIES")
config_book_series_uri = config_object["BOOK_DATA"].getboolean("BOOK_SERIES_URI")
config_isbn = config_object["BOOK_DATA"].getboolean("ISBN")
config_isbn13 = config_object["BOOK_DATA"].getboolean("ISBN13")
config_year_first_published = config_object["BOOK_DATA"].getboolean(
    "YEAR_FIRST_PUBLISHED"
)
config_author = config_object["BOOK_DATA"].getboolean("AUTHOR")
config_num_pages = config_object["BOOK_DATA"].getboolean("NUM_PAGES")
config_genres = config_object["BOOK_DATA"].getboolean("GENRES")
config_primary_genre = config_object["BOOK_DATA"].getboolean("PRIMARY_GENRE")
config_shelves = config_object["BOOK_DATA"].getboolean("SHELVES")
config_lists = config_object["BOOK_DATA"].getboolean("LISTS")
config_num_ratings = config_object["BOOK_DATA"].getboolean("NUM_RATINGS")
config_num_reviews = config_object["BOOK_DATA"].getboolean("NUM_REVIEWS")
config_average_rating = config_object["BOOK_DATA"].getboolean("AVERAGE_RATING")
config_rating_distribution = config_object["BOOK_DATA"].getboolean(
    "RATING_DISTRIBUTION"
)
