import pytest

from src.book_id.query.query_model import QueryModel
from src.book_id.result.match_service import get_match
from src.book_id.result.result_model import ResultModel


class TestResultMatchService:
    def setup_method(self):

        self.kafka_query_model = QueryModel(
            book_title="Amerika",
            author_name="Franz Kafka",
            book_title_minus_subtitle=None,
            book_title_and_author_name_search_url="https://www.goodreads.com/search?q=Amerika%20-%20Franz%20Kafka",
            book_title_search_url="https://www.goodreads.com/search?q=Amerika",
            book_title_minus_subtitle_search_url=None,
        )

        self.kafka_query_model_without_author = QueryModel(
            book_title="Amerika",
            author_name="",
            book_title_minus_subtitle=None,
            book_title_and_author_name_search_url="https://www.goodreads.com/search?q=Amerika%20-%20Franz%20Kafka",
            book_title_search_url="https://www.goodreads.com/search?q=Amerika",
            book_title_minus_subtitle_search_url=None,
        )

        self.kafka_result_models = [
            ResultModel(
                book_title='Technikbilder Und Technikkritik in Romanfragment "Der Verschollene" ("Amerika") Von Franz Kafka',
                author_name="Doreen Friebe",
                book_id="40316304-technikbilder-und-technikkritik-in-romanfragment-der-verschollene-am",
            ),
            ResultModel(
                book_title="Der Verschollene (Amerika) von Franz Kafka.: Textanalyse und Interpretation mit ausführlicher Inhaltsangabe und Abituraufgaben mit Lösungen (Königs Erläuterungen 497)",
                author_name="Daniel Rothenbühler",
                book_id="24105853-der-verschollene-amerika-von-franz-kafka",
            ),
            ResultModel(
                book_title="Amerika", author_name="Franz Kafka", book_id="22911.Amerika"
            ),
        ]

        self.kafka_result_match = ResultModel(
            book_title="Amerika", author_name="Franz Kafka", book_id="22911.Amerika"
        )

        self.empty_list = []

    def test_get_match_returns_none_where_result_models_are_empty(
        self,
    ):
        assert get_match(self.kafka_query_model, None, 1.0, 1.0) is None

    def test_get_match_returns_a_match_where_book_title_and_author_name_match_query_exactly(
        self,
    ):
        assert (
            get_match(self.kafka_query_model, self.kafka_result_models, 1.0, 1.0)
            == self.kafka_result_match
        )
