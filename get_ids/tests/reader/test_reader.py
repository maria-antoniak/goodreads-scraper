import pytest
from mock import mock_open, patch

from get_ids.reader.exceptions import InputFileIsEmpty
from get_ids.reader.reader import (_filter_queries_equal_to_none,
                           _get_queries_from_input_file, _is_file_empty,
                           _is_query_equal_to_none_present_in_queries,
                           read_file)


class TestReader:
    def setup_method(self):
        self.mock_path_to_file = "mock/path/to/file"
        self.EMPTY_FILE = 0
        self.SINGLE_QUERY = 3  # Corresponds to shortest imaginable query `a-a`.
        self.MULTIPLE_QUERIES = 50000  # Corresponds to a file containing 1000 queries.

        self.queries_without_none = ["Going After Cacciato - Tim O'Brien"]
        self.queries_with_none = ["Going After Cacciato - Tim O'Brien", None]
        self.multiline_queries_without_none = "The Catcher in the Rye - J.D Salinger\nEternal Curse on the Reader of These Pages - Manual Puig\n"
        self.multiline_queries_with_none = None

    def test_ut_get_queries_from_input_file_should_return_a_list_of_lines(self):
        mock = mock_open(read_data="Reasons to Live - Amy Hempl")
        with patch("get_ids.reader.reader.codecs.open", mock):
            assert _get_queries_from_input_file(self.mock_path_to_file) == [
                "Reasons to Live - Amy Hempl"
            ]

    def test_ut_get_queries_from_input_file_should_return_a_list_of_stripped_lines(
        self,
    ):
        mock = mock_open(read_data=self.multiline_queries_without_none)
        with patch("get_ids.reader.reader.codecs.open", mock):
            assert _get_queries_from_input_file(self.mock_path_to_file) == [
                "The Catcher in the Rye - J.D Salinger",
                "Eternal Curse on the Reader of These Pages - Manual Puig",
            ]

    def test_ut_is_file_empty_should_return_true_where_file_is_empty(self):
        with patch("os.path.getsize", return_value=self.EMPTY_FILE):
            assert _is_file_empty(self.mock_path_to_file) is True

    def test_ut_is_file_empty_should_return_false_where_file_is_not_empty_at_lower_boundary(
        self,
    ):
        with patch("os.path.getsize", return_value=self.SINGLE_QUERY):
            assert _is_file_empty(self.mock_path_to_file) is False

    def test_ut_is_file_empty_should_return_false_where_file_is_not_empty_at_upper_boundary(
        self,
    ):
        with patch("os.path.getsize", return_value=self.MULTIPLE_QUERIES):
            assert _is_file_empty(self.mock_path_to_file) is False

    def test_ut_is_query_equal_to_none_present_in_queries_should_return_true_where_query_query_equal_to_none_is_present(
        self,
    ):
        assert (
            _is_query_equal_to_none_present_in_queries(self.queries_with_none) is True
        )

    def test_ut_is_query_equal_to_none_should_return_false_where_query_is_not_none(
        self,
    ):
        assert (
            _is_query_equal_to_none_present_in_queries(self.queries_without_none)
            is False
        )

    def test_ut_filter_queries_equal_to_none_should_remove_queries_equal_to_none(self):
        assert (
            _filter_queries_equal_to_none(self.queries_with_none)
            == self.queries_without_none
        )

    def test_it_read_file_should_raise_input_file_is_empty_exception_where_file_is_empty(
        self,
    ):
        with pytest.raises(InputFileIsEmpty):
            with patch("os.path.getsize", return_value=self.EMPTY_FILE):
                read_file(self.mock_path_to_file)

    def test_it_read_file_should_raise_file_not_found_error_where_file_is_not_found(
        self,
    ):
        with pytest.raises(FileNotFoundError):
            read_file(self.mock_path_to_file)

    def test_it_read_file_should_raise_print_custom_file_not_found_error_message_where_file_is_not_found(
        self,
    ):
        with pytest.raises(
            FileNotFoundError,
            match=f"Please check '{self.mock_path_to_file}' is a valid path",
        ):
            read_file(self.mock_path_to_file)

    def test_it_read_file_should_remove_queries_equal_to_none(self):
        with patch("os.path.getsize", return_value=self.SINGLE_QUERY):

            mock = mock_open(read_data=self.multiline_queries_with_none)
            with patch("get_ids.reader.reader.codecs.open", mock):
                assert read_file(self.mock_path_to_file) == []

    def test_it_read_file_should_return_queries_where_no_queries_are_equal_to_none(
        self,
    ):
        with patch("os.path.getsize", return_value=self.SINGLE_QUERY):
            mock = mock_open(read_data=self.multiline_queries_without_none)
            with patch("get_ids.reader.reader.codecs.open", mock):
                assert read_file(self.mock_path_to_file) == [
                    "The Catcher in the Rye - J.D Salinger",
                    "Eternal Curse on the Reader of These Pages - Manual Puig",
                ]
