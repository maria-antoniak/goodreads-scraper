import pytest

from get_ids.models.query_model import QueryModel
from get_ids.query.query_model_builder import (_build_search_url_from_query,
                                       _is_subtitle_in_book_title,
                                       _remove_subtitle_from_book_title,
                                       _split_on_last_delimiter,
                                       build_query_model)


class TestQueryModelBuilder:
    def setup_method(self):
        self.query_with_single_delimiter = "Kitchen - Banana Yoshimoto"
        self.query_with_multiple_delimiters = (
            "63, Dream Palace: Selected Stories, 1956-1987 - James Purdy"
        )
        self.delimiter = " - "
        self.book_title_with_colon_subtitle = (
            "An Individual Note: Of Music, Sound And Electronics"
        )
        self.book_title_with_semi_colon_subtitle = "The Diary of a Madman and Other Stories: The Nose; The Carriage; The Overcoat; Taras Bulba"
        self.book_title_with_parenthesis_subtitle = "Palace Walk (The Cairo Trilogy #1)"
        self.book_title_with_parenthesis_subtitle_false_positive = "H(A)PPY"
        self.book_title_without_subtitle = "My Year of Rest and Relaxation"

    def test_ut_split_on_last_delimiter_should_return_book_title_and_author_where_the_delimiter_appears_once(
        self,
    ):
        assert _split_on_last_delimiter(
            self.query_with_single_delimiter, self.delimiter
        ) == ["Kitchen", "Banana Yoshimoto"]

    @pytest.mark.parametrize(
        "query, expected",
        [
            (
                "63, Dream Palace: Selected Stories, 1956-1987 - James Purdy",
                ["63, Dream Palace: Selected Stories, 1956-1987", "James Purdy"],
            ),
            (
                "A Portrait of the Artist as a Young Man: By James Joyce - Illustrated - James Joyce",
                [
                    "A Portrait of the Artist as a Young Man: By James Joyce - Illustrated",
                    "James Joyce",
                ],
            ),
            (
                "Catch-22 - Joseph Heller",
                [
                    "Catch-22",
                    "Joseph Heller",
                ],
            ),
        ],
    )
    def test_ut_split_on_last_delimiter_should_return_book_title_and_author_where_the_delimiter_appears_twice(
        self, query, expected
    ):
        assert _split_on_last_delimiter(query, self.delimiter) == expected

    def test_ut_is_subtitle_in_book_title_should_return_true_where_a_colon_subtitle_is_in_the_book_title(
        self,
    ):
        assert _is_subtitle_in_book_title(self.book_title_with_colon_subtitle) is True

    def test_ut_is_subtitle_in_book_title_should_return_true_where_a_semi_colon_subtitle_is_in_the_book_title(
        self,
    ):
        assert (
            _is_subtitle_in_book_title(self.book_title_with_semi_colon_subtitle) is True
        )

    def test_ut_is_subtitle_in_book_title_should_return_true_where_a_parenthesis_subtitle_is_in_the_book_title(
        self,
    ):
        assert (
            _is_subtitle_in_book_title(self.book_title_with_parenthesis_subtitle)
            is True
        )

    def test_ut_is_subtitle_in_book_title_should_return_false_where_no_subtitle_is_in_the_book_title(
        self,
    ):
        assert _is_subtitle_in_book_title(self.book_title_without_subtitle) is False

    def test_ut_is_subtitle_in_book_title_should_return_false_where_book_title_is_a_false_positive(
        self,
    ):
        assert (
            _is_subtitle_in_book_title(
                self.book_title_with_parenthesis_subtitle_false_positive
            )
            is False
        )

    def test_ut_remove_subtitle_from_book_title_should_remove_a_colon_subtitle_if_in_the_book_title(
        self,
    ):
        assert (
            _remove_subtitle_from_book_title(self.book_title_with_colon_subtitle)
            == "An Individual Note"
        )

    def test_ut_remove_subtitle_from_book_title_should_remove_a_semi_colon_subtitle_if_in_the_book_title(
        self,
    ):
        assert (
            _remove_subtitle_from_book_title(self.book_title_with_semi_colon_subtitle)
            == "The Diary of a Madman and Other Stories"
        )

    def test_ut_remove_subtitle_from_book_title_should_remove_a_parenthesis_subtitle_if_in_the_book_title(
        self,
    ):
        assert (
            _remove_subtitle_from_book_title(self.book_title_with_parenthesis_subtitle)
            == "Palace Walk"
        )

    def test_it_build_search_url_from_query_should_return_encoded_query_where_query_is_not_none(
        self,
    ):
        result = "https://www.goodreads.com/search?q=H%28A%29PPY"
        assert (
            _build_search_url_from_query(
                self.book_title_with_parenthesis_subtitle_false_positive
            )
            == result
        )

    def test_it_build_search_url_from_query_should_not_return_encoded_query_where_query_is_none(
        self,
    ):
        assert _build_search_url_from_query(None) is None

    def test_it_build_query_model_should_return_a_query_model_where_book_title_does_not_contain_a_subtitle(
        self,
    ):
        query_model = QueryModel(
            book_title="Kitchen",
            author_name="Banana Yoshimoto",
            book_title_minus_subtitle=None,
            book_title_and_author_name_search_url="https://www.goodreads.com/search?q=Kitchen%20-%20Banana%20Yoshimoto",
            book_title_search_url="https://www.goodreads.com/search?q=Kitchen",
            book_title_minus_subtitle_search_url=None,
        )

        assert (
            build_query_model(self.query_with_single_delimiter, self.delimiter)
            == query_model
        )

    def test_it_build_query_model_should_return_a_query_model_where_book_title_contains_a_subtitle(
        self,
    ):
        query_model = QueryModel(
            book_title="63, Dream Palace: Selected Stories, 1956-1987",
            author_name="James Purdy",
            book_title_minus_subtitle="63, Dream Palace",
            book_title_and_author_name_search_url="https://www.goodreads.com/search?q=63%2C%20Dream%20Palace%3A%20Selected%20Stories%2C%201956-1987%20-%20James%20Purdy",
            book_title_search_url="https://www.goodreads.com/search?q=63%2C%20Dream%20Palace%3A%20Selected%20Stories%2C%201956-1987",
            book_title_minus_subtitle_search_url="https://www.goodreads.com/search?q=63%2C%20Dream%20Palace",
        )

        assert (
            build_query_model(self.query_with_multiple_delimiters, self.delimiter)
            == query_model
        )
