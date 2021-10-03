import pytest

from src.book_id.query.query_service import QueryService


class TestQueryService:
    def setup_method(self):

        self.query_with_single_delimiter = "Kitchen - Banana Yoshimoto"
        self.query_with_multiple_delimiters = (
            "63, Dream Palace: Selected Stories, 1956-1987 - James Purdy"
        )

        self.book_title_with_colon_subtitle = (
            "An Individual Note: Of Music, Sound And Electronics"
        )
        self.book_title_with_semi_colon_subtitle = "The Diary of a Madman and Other Stories: The Nose; The Carriage; The Overcoat; Taras Bulba"
        self.book_title_with_parenthesis_subtitle = "Palace Walk (The Cairo Trilogy #1)"
        self.book_title_with_parenthesis_subtitle_false_positive = "H(A)PPY"
        self.book_title_without_subtitle = "My Year of Rest and Relaxation"

    def test_split_on_last_delimiter_should_return_book_title_and_author_where_the_delimiter_appears_once(
        self,
    ):
        query_service = QueryService(self.query_with_single_delimiter)
        assert query_service._split_on_last_delimiter() == [
            "Kitchen",
            "Banana Yoshimoto",
        ]

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
    def test_split_on_last_delimiter_should_return_book_title_and_author_where_the_delimiter_appears_twice(
        self, query, expected
    ):

        query_service = QueryService(query)

        assert query_service._split_on_last_delimiter() == expected

    def test_is_subtitle_in_book_title_should_return_true_where_a_colon_subtitle_is_in_the_book_title(
        self,
    ):
        query_service = QueryService(self.book_title_with_colon_subtitle)

        assert (
            query_service._is_subtitle_in_book_title(
                self.book_title_with_colon_subtitle
            )
            is True
        )

    def test_is_subtitle_in_book_title_should_return_true_where_a_semi_colon_subtitle_is_in_the_book_title(
        self,
    ):

        query_service = QueryService(self.book_title_with_semi_colon_subtitle)

        assert (
            query_service._is_subtitle_in_book_title(
                self.book_title_with_semi_colon_subtitle
            )
            is True
        )

    def test_is_subtitle_in_book_title_should_return_true_where_a_parenthesis_subtitle_is_in_the_book_title(
        self,
    ):
        query_service = QueryService(self.book_title_with_parenthesis_subtitle)

        assert (
            query_service._is_subtitle_in_book_title(
                self.book_title_with_parenthesis_subtitle
            )
            is True
        )

    def test_is_subtitle_in_book_title_should_return_false_where_no_subtitle_is_in_the_book_title(
        self,
    ):

        query_service = QueryService(self.book_title_without_subtitle)

        assert (
            query_service._is_subtitle_in_book_title(self.book_title_without_subtitle)
            is False
        )

    def test_is_subtitle_in_book_title_should_return_false_where_book_title_is_a_false_positive(
        self,
    ):

        query_service = QueryService(
            self.book_title_with_parenthesis_subtitle_false_positive
        )

        assert (
            query_service._is_subtitle_in_book_title(
                self.book_title_with_parenthesis_subtitle_false_positive
            )
            is False
        )

    def test_remove_subtitle_from_book_title_should_remove_a_colon_subtitle_if_in_the_book_title(
        self,
    ):

        query_service = QueryService(self.book_title_with_colon_subtitle)

        assert (
            query_service._remove_subtitle_from_book_title(
                self.book_title_with_colon_subtitle
            )
            == "An Individual Note"
        )

    def test_remove_subtitle_from_book_title_should_remove_a_semi_colon_subtitle_if_in_the_book_title(
        self,
    ):

        query_service = QueryService(self.book_title_with_semi_colon_subtitle)

        assert (
            query_service._remove_subtitle_from_book_title(
                self.book_title_with_semi_colon_subtitle
            )
            == "The Diary of a Madman and Other Stories"
        )

    def test_remove_subtitle_from_book_title_should_remove_a_parenthesis_subtitle_if_in_the_book_title(
        self,
    ):
        query_service = QueryService(self.book_title_with_parenthesis_subtitle)

        assert (
            query_service._remove_subtitle_from_book_title(
                self.book_title_with_parenthesis_subtitle
            )
            == "Palace Walk"
        )

    def test_build_search_url_from_query_should_return_encoded_query_where_query_is_not_none(
        self,
    ):
        query_service = QueryService(
            self.book_title_with_parenthesis_subtitle_false_positive
        )

        result = "https://www.goodreads.com/search?q=H%28A%29PPY"
        assert (
            query_service._build_search_url_from_query(
                self.book_title_with_parenthesis_subtitle_false_positive
            )
            == result
        )

    def test_build_search_url_from_query_should_not_return_encoded_query_where_query_is_none(
        self,
    ):
        query_service = QueryService(None)

        assert query_service._build_search_url_from_query(None) is None
