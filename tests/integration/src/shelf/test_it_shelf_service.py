from data.all_the_pretty_horses_shelves import \
    all_the_pretty_horses_shelves_soup
from data.empty import empty_soup

from src.shelf.shelf_service import ShelfService


class TestBookService:
    def setup_method(self):
        self.shelf_service = ShelfService(all_the_pretty_horses_shelves_soup)
        self.shelf_service_empty = ShelfService(empty_soup)
        self.shelf = "to-read 61,056 people"

    def test_get_shelves(self):
        expected = [
            {"AmountOfUsersWhoAddedBookToList": 61211, "shelfName": "to-read"},
            {"AmountOfUsersWhoAddedBookToList": 3989, "shelfName": "currently-reading"},
            {"AmountOfUsersWhoAddedBookToList": 2581, "shelfName": "fiction"},
            {"AmountOfUsersWhoAddedBookToList": 1013, "shelfName": "favorites"},
            {"AmountOfUsersWhoAddedBookToList": 782, "shelfName": "western"},
            {"AmountOfUsersWhoAddedBookToList": 495, "shelfName": "own"},
            {"AmountOfUsersWhoAddedBookToList": 430, "shelfName": "owned"},
            {"AmountOfUsersWhoAddedBookToList": 424, "shelfName": "historical-fiction"},
            {"AmountOfUsersWhoAddedBookToList": 399, "shelfName": "classics"},
            {"AmountOfUsersWhoAddedBookToList": 294, "shelfName": "literature"},
        ]
        assert self.shelf_service.get_shelves() == expected
