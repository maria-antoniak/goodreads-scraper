from data.empty import empty_soup
from data.franz_kafka_wikipedia_page import franz_kafka_wikipedia_page_soup

from src.author.author_service import AuthorService


class TestAuthorService:
    def setup_method(self):

        self.author_service = AuthorService(
            "Franz Kafka", franz_kafka_wikipedia_page_soup
        )
        self.author_service_empty = AuthorService("Franz Kafka", empty_soup)

    def test_get_date_of_birth(self):
        assert self.author_service.get_date_of_birth() == "1883-07-03"

    def test_get_date_of_birth_should_return_none_where_soup_find_fails(self):
        assert self.author_service_empty.get_date_of_birth() is None
