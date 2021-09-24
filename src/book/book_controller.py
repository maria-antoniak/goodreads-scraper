# Call service that actually does the thing

import time

from book_service import BookService

from src.common.parser.parser import parse

from .config.config import (
    config_author,
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


def scrape_book(book_id_title):
    soup = parse(book_id_title)

    book_service = BookService(soup)

    time.sleep(2)

    return {
        "book_id_title": book_id_title if config_book_id_title is True else None,
        "numeric_book_id": book_service.get_numeric_id()
        if config_numeric_book_id is True
        else None,
        "book_title": book_service.get_title() if config_book_title is True else None,
        "book_series": book_service.get_book_series()
        if config_book_series is True
        else None,
        "book_series_uri": book_service.get_series_uri()
        if config_book_series_uri is True
        else None,
        "isbn": book_service.get_isbn() if config_isbn is True else None,
        "isbn13": book_service.get_isbn13() if config_isbn13 is True else None,
        "year_first_published": book_service.get_year_first_published()
        if config_year_first_published is True
        else None,
        "author": book_service.get_author() if config_author is True else None,
        "num_pages": book_service.get_number_of_pages()
        if config_num_pages is True
        else None,
        "genres": book_service.get_genres() if config_genres is True else None,
        "primary_genre": book_service.get_primary_genre()
        if config_primary_genre is True
        else None,
        "shelves": book_service.get_shelves() if config_shelves is True else None,
        "lists": book_service.get_lists() if config_lists is True else None,
        "num_ratings": book_service.get_number_of_ratings()
        if config_num_ratings is True
        else None,
        "num_reviews": book_service.get_number_of_reviews()
        if config_num_reviews is True
        else None,
        "average_rating": book_service.get_average_rating()
        if config_average_rating is True
        else None,
        "rating_distribution": book_service.get_rating_distribution()
        if config_rating_distribution is True
        else None,
    }


# print(scrape_book("636223.Ice"))
