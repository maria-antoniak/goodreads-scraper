# Call service that actually does the thing
import pprint

from src.book.book_config import *
from src.book.book_model import BookModel
from src.book.book_service import BookService
from src.common.formatters.json.to_json import to_json
from src.common.network.network import get
from src.common.parser.parser import parse
from src.common.utils.time_it import timeit
from typing import Dict
from src.list.list_service import ListService
from src.shelf.shelf_service import ShelfService


@timeit
def build_book_model(book_id_title: str) -> Dict:

    BASE = "https://www.goodreads.com/book/show/"
    url = f"{BASE}{book_id_title}"

    response = get([url])
    soup = parse(response[0])

    book_service = BookService(soup)
    shelf_service = ShelfService(soup)

    author_full_name = (
        book_service.get_author_full_name() if config_author_full_name is True else None
    )

    genres = book_service.get_genres() if config_genres is True else None

    lists_url = book_service.get_lists_url() if config_lists_url is True else None

    response = get([lists_url])
    soup = parse(response[0])

    lists_service = ListService(soup, lists_url)


    book_model = BookModel(
        author_first_name=book_service.get_author_first_name(author_full_name)
        if config_author_first_name is True
        else None,
        author_full_name=author_full_name,
        author_last_name=book_service.get_author_last_name(author_full_name)
        if config_author_last_name is True
        else None,
        average_rating=book_service.get_average_rating()
        if config_average_rating is True
        else None,
        genres=genres,
        isbn13=book_service.get_isbn13() if config_isbn13 is True else None,
        isbn=book_service.get_isbn() if config_isbn is True else None,
        lists=lists_service.get_lists() if config_lists is True else None,
        number_of_pages=book_service.get_number_of_pages()
        if config_number_of_pages is True
        else None,
        number_of_ratings=book_service.get_number_of_ratings()
        if config_number_of_ratings is True
        else None,
        number_of_reviews=book_service.get_number_of_reviews()
        if config_number_of_reviews is True
        else None,
        numeric_id=book_service.get_numeric_id(book_id_title)
        if config_numeric_id is True
        else None,
        primary_genre=book_service.get_primary_genre(genres)
        if config_primary_genre is True
        else None,
        rating_distribution=book_service.get_rating_distribution()
        if config_rating_distribution is True
        else None,
        series_name=book_service.get_series_name()
        if config_series_name is True
        else None,
        series_url=book_service.get_series_url() if config_series_url is True else None,
        shelves=shelf_service.get_shelves() if config_shelves is True else None,
        title=book_service.get_title() if config_title is True else None,
        title_id=book_id_title if config_title_id is True else None,
        year_of_publication=book_service.get_year_of_publication()
        if config_year_of_publication is True
        else None,
    )

    model = book_model
    result = to_json(model)
    pprint.pprint(result, indent=4)
    return result
