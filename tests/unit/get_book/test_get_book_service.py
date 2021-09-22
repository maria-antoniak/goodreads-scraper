from src.books.book_service import BookService
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
        self.book_service = BookService(all_the_pretty_horses_soup)
        self.book_service_empty = BookService(empty_soup)
        self.shelf = "to-read 61,056 people"

    def test_get_numeric_book_id(self):
        assert self.book_service.get_numeric_id(self.book_id_title) == 469571

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

    def test_get_shelves_url(self):
        assert (
            self.book_service._get_shelves_url()
            == "https://www.goodreads.com/book/shelves/469571.All_the_Pretty_Horses"
        )

    def test_get_shelves_url_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty._get_shelves_url() is None

    def test_get_unformatted_shelves(self):
        expected = [
            "to-read 61,056 people",
            "currently-reading 3,986 people",
            "fiction 2,577 people",
            "favorites 1,009 people",
            "western 778 people",
            "own 494 people",
            "owned 429 people",
            "historical-fiction 423 people",
            "classics 398 people",
            "literature 292 people",
            "books-i-own 244 people",
            "westerns 222 people",
            "novels 221 people",
            "literary-fiction 163 people",
            "book-club 163 people",
            "national-book-award 160 people",
            "library 151 people",
            "american 149 people",
            "cormac-mccarthy 144 people",
            "1001-books 133 people",
            "series 129 people",
            "2020 120 people",
            "contemporary 117 people",
            "adventure 109 people",
            "2021 108 people",
            "mexico 107 people",
            "novel 103 people",
            "literary 102 people",
            "owned-books 100 people",
            "kindle 98 people",
            "american-literature 98 people",
            "audiobook 96 people",
            "2018 94 people",
            "2019 92 people",
            "2017 90 people",
            "1001 90 people",
            "contemporary-fiction 87 people",
            "school 86 people",
            "historical 85 people",
            "texas 84 people",
            "audiobooks 81 people",
            "2016 78 people",
            "ebook 77 people",
            "general-fiction 77 people",
            "abandoned 75 people",
            "2014 74 people",
            "2013 74 people",
            "wishlist 73 people",
            "my-library 72 people",
            "coming-of-age 71 people",
            "2015 70 people",
            "adult-fiction 70 people",
            "default 69 people",
            "audio 68 people",
            "american-lit 66 people",
            "20th-century 66 people",
            "2012 64 people",
            "usa 63 people",
            "favourites 62 people",
            "audible 57 people",
            "classic 57 people",
            "romance 55 people",
            "1001-books-to-read-before-you-die 54 people",
            "2011 53 people",
            "to-buy 53 people",
            "did-not-finish 49 people",
            "adult 48 people",
            "american-west 48 people",
            "high-school 47 people",
            "to-read-fiction 46 people",
            "2010 46 people",
            "americana 46 people",
            "mccarthy 46 people",
            "read-for-school 43 people",
            "ebooks 41 people",
            "my-books 41 people",
            "1990s 40 people",
            "dnf 38 people",
            "home-library 35 people",
            "modern-fiction 35 people",
            "lit 34 people",
            "america 33 people",
            "national-book-award-winners 33 people",
            "horses 32 people",
            "southern-gothic 32 people",
            "general 31 people",
            "cowboys 31 people",
            "bookshelf 31 people",
            "american-fiction 30 people",
            "school-books 28 people",
            "all-time-favorites 28 people",
            "ap-lit 27 people",
            "award-winners 27 people",
            "bookclub 27 people",
            "calibre 26 people",
            "coming 26 people",
            "audio-book 26 people",
            "2009 26 people",
            "1001-books-you-must-read-before-you 25 people",
            "of 25 people",
        ]
        assert (
            self.book_service._get_unformatted_shelves(
                all_the_pretty_horses_shelves_soup
            )
            == expected
        )

    def test_get_unformatted_shelves_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty._get_unformatted_shelves() is None

    def test_get_shelf_name(self):
        assert self.book_service._get_shelf_name(self.shelf) == "to-read"

    def test_get_shelf_count(self):
        assert self.book_service._get_shelf_count(self.shelf) == 61056

    def test_get_lists_url(self):
        assert self.book_service._get_lists_url(self) == "https://www.goodreads.com/list/book/469571"

    def test_get_lists_url_should_return_none_where_soup_find_fails(self):
        assert self.book_service_empty._get_lists_url(self) is None

    def test_get_paginated_list_urls(self):
        url = "https://www.goodreads.com/list/book/469571"
        expected = [url, 'https://www.goodreads.com/list/book/469571?page=2', 'https://www.goodreads.com/list/book/469571?page=3', 'https://www.goodreads.com/list/book/469571?page=4', 'https://www.goodreads.com/list/book/469571?page=5', 'https://www.goodreads.com/list/book/469571?page=6', 'https://www.goodreads.com/list/book/469571?page=7', 'https://www.goodreads.com/list/book/469571?page=8', 'https://www.goodreads.com/list/book/469571?page=9']
        assert self.book_service._get_paginated_list_urls(all_the_pretty_horses_lists_soup, url) == expected

    def test_get_paginated_list_urls_should_return_none_where_soup_find_fails(self):
        url = "https://www.goodreads.com/list/book/469571"
        assert self.book_service_empty._get_paginated_list_urls(empty_soup, url) is None