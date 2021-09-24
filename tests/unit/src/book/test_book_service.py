from src.book.service.book_service import BookService
from data.all_the_pretty_horses import (
    all_the_pretty_horses_soup,
    all_the_pretty_horses_shelves_soup,
    all_the_pretty_horses_lists_soup
)
from data.empty import empty_soup
import pytest


class TestBookService:
    def setup_method(self):
        self.book_id_title = "469571.All_the_Pretty_Horses"
        self.book_id_title_without_decimal = "13079982-fahrenheit-451"
        self.book_service = BookService(all_the_pretty_horses_soup)
        self.book_service_empty = BookService(empty_soup)
        self.shelf = "to-read 61,056 people"

    def test_get_numeric_book_id(self):
        assert self.book_service.get_numeric_id(self.book_id_title) == 469571

    def test_get_numeric_book_id_where_no_decimal_is_present(self):
        assert self.book_service.get_numeric_id(self.book_id_title_without_decimal) == 13079982

    def test_get_book_title(self):
        assert self.book_service.get_title() == "All the Pretty Horses"

    def test_get_book_title_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_title() is None

    def test_get_book_series_name(self):
        assert self.book_service.get_series_name() == "The Border Trilogy #1"

    def test_get_book_series_name_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_series_name() is None

    def test_get_book_series_uri(self):
        assert (
            self.book_service.get_series_uri()
            == "https://www.goodreads.com/series/44780-the-border-trilogy"
        )

    def test_get_book_series_uri_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_series_uri() is None

    def test_get_isbn(self):
        assert self.book_service.get_isbn() == int("0330510932")

    def test_get_isbn_should_return_none_where_soup_findall_fails(self):
        assert self.book_service_empty.get_isbn() is None

    def test_get_isbn13(self):
        assert self.book_service.get_isbn13() == 9780330510936

    def test_get_isbn13_should_return_none_where_soup_findall_fails(self):
        assert self.book_service_empty.get_isbn() is None

    def test_get_year_first_published(self):
        assert self.book_service.get_year_first_published() == 1992

    def test_get_year_first_published_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_year_first_published() is None

    def test_get_author_full_name(self):
        assert self.book_service.get_author_full_name() == "Cormac McCarthy"

    def test_get_author_full_name_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_author_full_name() is None

    full_names_to_first_names = [
        ("Cormac McCarthy", "Cormac"),
        ("Jean-Jacques Rousseau", "Jean-Jacques"),
        ("G.A. Cohen", "G.A."),
        ("Olav H. Hauge", "Olav"),
        ("P.M.", "P.M."),
        ("Aeschylus", "Aeschylus"),
    ]

    @pytest.mark.parametrize("full_name, expected", full_names_to_first_names)
    def test_get_author_first_name(self, full_name, expected):
        assert self.book_service.get_author_first_name(full_name) == expected

    full_names_to_last_names = [
        ("Cormac McCarthy", "McCarthy"),
        ("Jean-Jacques Rousseau", "Rousseau"),
        ("G.A. Cohen", "Cohen"),
        ("Olav H. Hauge", "Hauge"),
        ("P.M.", ""),
        ("Aeschylus", ""),
    ]

    @pytest.mark.parametrize("full_name, expected", full_names_to_last_names)
    def test_get_author_last_name(self, full_name, expected):
        assert self.book_service.get_author_last_name(full_name) == expected

    def test_get_number_of_pages(self):
        assert self.book_service.get_number_of_pages() == 302

    def test_get_number_of_pages_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_number_of_pages() is None

    def test_get_genres(self):
        expected = [
            "Fiction",
            "Westerns",
            "Historical > Historical Fiction",
            "Classics",
            "Literature",
            "Novels",
            "Literary Fiction",
            "Literature > American",
            "Contemporary",
            "Adventure",
        ]
        assert self.book_service.get_genres() == expected

    def test_get_genres_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_number_of_pages() is None

    def test_get_primary_genre(self):
        genre_list = [
            "Fiction",
            "Westerns",
            "Historical > Historical Fiction",
            "Classics",
            "Literature",
            "Novels",
            "Literary Fiction",
            "Literature > American",
            "Contemporary",
            "Adventure",
        ]
        assert self.book_service.get_primary_genre(genre_list) == "Fiction"

    def test_get_primary_genre_should_return_none_where_genre_list_is_empty(self):
        assert self.book_service_empty.get_number_of_pages() is None

    def test_get_lists_url(self):
        assert self.book_service.get_lists_url() == "https://www.goodreads.com/list/book/469571"

    def test_get_lists_url_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty.get_lists_url() is None

    # def test_get_lists_url(self):
    #     assert self.book_service._get_lists_url(self) == "https://www.goodreads.com/list/book/469571"
    #
    # def test_get_lists_url_should_return_none_where_soup_find_fails(self):
    #     assert self.book_service_empty._get_lists_url(self) is None
    #
    # def test_get_paginated_list_urls(self):
    #     url = "https://www.goodreads.com/list/book/469571"
    #     expected = [url, 'https://www.goodreads.com/list/book/469571?page=2', 'https://www.goodreads.com/list/book/469571?page=3', 'https://www.goodreads.com/list/book/469571?page=4', 'https://www.goodreads.com/list/book/469571?page=5', 'https://www.goodreads.com/list/book/469571?page=6', 'https://www.goodreads.com/list/book/469571?page=7', 'https://www.goodreads.com/list/book/469571?page=8', 'https://www.goodreads.com/list/book/469571?page=9']
    #     assert self.book_service._get_paginated_list_urls(all_the_pretty_horses_lists_soup, url) == expected
    #
    # def test_get_paginated_list_urls_should_return_none_where_soup_find_fails(self):
    #     url = "https://www.goodreads.com/list/book/469571"
    #     assert self.book_service_empty._get_paginated_list_urls(empty_soup, url) is None