from data.all_the_pretty_horses import all_the_pretty_horses_shelves_soup
from data.empty import empty_soup

from src.shelf.shelf_service import ShelfService


class TestBookService:
    def setup_method(self):
        self.shelf_service = ShelfService(all_the_pretty_horses_shelves_soup)
        self.shelf_service_empty = ShelfService(empty_soup)
        self.shelf = "to-read 61,056 people"

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
        assert self.shelf_service._get_unformatted_shelves() == expected

    def test_get_unformatted_shelves_should_return_empty_where_soup_find_all_fails(
        self,
    ):
        assert self.shelf_service_empty._get_unformatted_shelves() == []

    def test_get_shelf_name(self):
        assert self.shelf_service._get_shelf_name(self.shelf) == "to-read"

    def test_get_shelf_count(self):
        assert self.shelf_service._get_shelf_count(self.shelf) == 61056
