# Call service that actually does the thing

import time

from src.book.service.book_service import BookService

from src.book.model.book_model import BookModel

from src.common.parser.parser import parse
from src.common.network.network import get

from src.book.config.book_config import (
    config_author_full_name,
    config_author_first_name,
    config_author_last_name,
    config_average_rating,
    config_book_id_title,
    config_book_series,
    config_book_series_uri,
    config_book_title,
    config_genres,
    config_isbn,
    config_isbn13,
    config_lists,
    config_num_pages,
    config_num_ratings,
    config_num_reviews,
    config_numeric_book_id,
    config_primary_genre,
    config_rating_distribution,
    config_shelves,
    config_year_first_published,
)

from src.common.utils.time_it import timeit

@timeit
def build_book_model(book_id_title):

    # This method will be called from main, i.e the view
    base = "https://www.goodreads.com/book/show/"
    url = f"{base}{book_id_title}"

    response = get([url])
    soup = parse(response[0])

    book_service = BookService(soup)

    genres = book_service.get_genres() if config_genres is True else None
    author_full_name = book_service.get_author_full_name() if config_author_full_name is True else None

    book_model = BookModel(
        title_id=book_id_title if config_book_id_title is True else None,
        numeric_id=book_service.get_numeric_id(book_id_title) if config_numeric_book_id is True else None,
        title=book_service.get_title() if config_book_title is True else None,
        series=book_service.get_series_name() if config_book_series is True else None,
        book_series_uri=book_service.get_series_uri() if config_book_series_uri is True else None,
        isbn=book_service.get_isbn() if config_isbn is True else None,
        isbn13=book_service.get_isbn13() if config_isbn13 is True else None,
        author_full_name=author_full_name,
        author_first_name=book_service.get_author_first_name(author_full_name) if config_author_first_name is True else None,
        author_last_name=book_service.get_author_last_name(author_full_name) if config_author_last_name is True else None,
        number_of_pages=book_service.get_number_of_pages() if config_num_pages is True else None,
        genres=genres,
        primary_genre=book_service.get_primary_genre(genres) if config_primary_genre is True else None,



    )
    from pprint import pprint
    from src.common.formatters.json.to_json import to_json

    result = book_model
    pprint(to_json(result))

    # return {
    #     "book_id_title": book_id_title if config_book_id_title is True else None,
    #     "numeric_book_id": book_service.get_numeric_id()
    #     if config_numeric_book_id is True
    #     else None,
    #     "book_title": book_service.get_title() if config_book_title is True else None,
    #     "book_series": book_service.get_book_series()
    #     if config_book_series is True
    #     else None,
    #     "book_series_uri": book_service.get_series_uri()
    #     if config_book_series_uri is True
    #     else None,
    #     "isbn": book_service.get_isbn() if config_isbn is True else None,
    #     "isbn13": book_service.get_isbn13() if config_isbn13 is True else None,
    #     "year_first_published": book_service.get_year_first_published()
    #     if config_year_first_published is True
    #     else None,
    #     "author": book_service.get_author() if config_author is True else None,
    #     "num_pages": book_service.get_number_of_pages()
    #     if config_num_pages is True
    #     else None,
    #     "genres": book_service.get_genres() if config_genres is True else None,
    #     "primary_genre": book_service.get_primary_genre()
    #     if config_primary_genre is True
    #     else None,
    #     "shelves": book_service.get_shelves() if config_shelves is True else None,
    #     "lists": book_service.get_lists() if config_lists is True else None,
    #     "num_ratings": book_service.get_number_of_ratings()
    #     if config_num_ratings is True
    #     else None,
    #     "num_reviews": book_service.get_number_of_reviews()
    #     if config_num_reviews is True
    #     else None,
    #     "average_rating": book_service.get_average_rating()
    #     if config_average_rating is True
    #     else None,
    #     "rating_distribution": book_service.get_rating_distribution()
    #     if config_rating_distribution is True
    #     else None,
    # }

#
# bs = "781410.Young_Adam"
# build_book_model(bs)