from data.all_the_pretty_horses import all_the_pretty_horses_lists_soup
from data.empty import empty_soup

from src.list.list_service import ListService


class TestListService:
    def setup_method(self):
        self.lists_url = "https://www.goodreads.com/list/book/469571"
        self.list_service = ListService(
            all_the_pretty_horses_lists_soup, self.lists_url
        )
        self.list_service_empty = ListService(empty_soup, self.lists_url)

    def test_get_paginated_list_urls(self):
        url = "https://www.goodreads.com/list/book/469571"
        expected = [
            url,
            "https://www.goodreads.com/list/book/469571?page=2",
            "https://www.goodreads.com/list/book/469571?page=3",
            "https://www.goodreads.com/list/book/469571?page=4",
            "https://www.goodreads.com/list/book/469571?page=5",
            "https://www.goodreads.com/list/book/469571?page=6",
            "https://www.goodreads.com/list/book/469571?page=7",
            "https://www.goodreads.com/list/book/469571?page=8",
            "https://www.goodreads.com/list/book/469571?page=9",
        ]
        assert (
            self.list_service._get_paginated_list_urls(
                all_the_pretty_horses_lists_soup, url
            )
            == expected
        )

    def test_get_paginated_list_urls_should_return_none_where_soup_find_fails(self):
        url = "https://www.goodreads.com/list/book/469571"
        assert self.list_service_empty._get_paginated_list_urls(empty_soup, url) is None
