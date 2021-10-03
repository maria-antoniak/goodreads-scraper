from src.book_id.query.query_model import QueryModel
from src.book_id.result.match_service import (_is_input_similar,
                                              _is_results_equal_to_one)
from src.book_id.result.result_model import ResultModel


class TestResultMatchHandler:
    def setup_method(self):
        self.result_model = [
            ResultModel(
                book_title="The Collected Letters of Flann O'Brien",
                author_name="Flann O'Brien",
                book_id="34415484-the-collected-letters-of-flann-o-brien",
            )
        ]

        self.kafka_query_model = QueryModel(
            book_title="Amerika",
            author_name="Franz Kafka",
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

    def test_is_results_equal_to_one_should_return_true_where_result_is_equal_to_one(
        self,
    ):
        assert _is_results_equal_to_one(self.result_model) is True

    def test_is_results_equal_to_one_should_return_false_where_result_is_not_equal_to_one(
        self,
    ):
        assert _is_results_equal_to_one(self.empty_list) is False

    def test_is_input_similar_returns_true_where_expecting_an_exact_match(self):
        assert _is_input_similar("Kitchen", "Kitchen", 1.0) is True

    def test_is_input_similar_returns_false_where_expecting_an_exact_match(self):
        assert _is_input_similar("Kitchen", "Kitchens", 1.0) is False

    def test_is_input_similar_returns_true_where_similarity_percentage_is_set_to_a_low_level_of_permissiveness(
        self,
    ):
        assert (
            _is_input_similar(
                "The Complete Plays", "The Complete Plays: Sophocles", 0.75
            )
            is True
        )

    def test_is_input_similar_returns_true_where_similarity_percentage_is_set_to_a_high_level_of_permissiveness(
        self,
    ):
        assert (
            _is_input_similar(
                "The Diary of a Madman",
                "The Diary of a Madman and Other Stories: The Nose; The Carriage; The Overcoat; Taras Bulbas",
                0.25,
            )
            is True
        )
