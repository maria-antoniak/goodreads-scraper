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
            {"AmountOfUsersWhoAddedBookToShelf": 61211, "shelfName": "to-read"},
            {
                "AmountOfUsersWhoAddedBookToShelf": 3989,
                "shelfName": "currently-reading",
            },
            {"AmountOfUsersWhoAddedBookToShelf": 2581, "shelfName": "fiction"},
            {"AmountOfUsersWhoAddedBookToShelf": 1013, "shelfName": "favorites"},
            {"AmountOfUsersWhoAddedBookToShelf": 782, "shelfName": "western"},
            {"AmountOfUsersWhoAddedBookToShelf": 495, "shelfName": "own"},
            {"AmountOfUsersWhoAddedBookToShelf": 430, "shelfName": "owned"},
            {
                "AmountOfUsersWhoAddedBookToShelf": 424,
                "shelfName": "historical-fiction",
            },
            {"AmountOfUsersWhoAddedBookToShelf": 399, "shelfName": "classics"},
            {"AmountOfUsersWhoAddedBookToShelf": 294, "shelfName": "literature"},
        ]
        assert self.shelf_service.get_shelves() == expected
