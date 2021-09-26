import pytest
from mock import mock_open, patch

from src.common.app_io.reader.exceptions import InputFileIsEmpty
from src.common.app_io.reader.reader import read_file


class TestReader:
    def setup_method(self):
        self.mock_path_to_file = "mock/path/to/file"
        self.EMPTY_FILE = 0
        self.SINGLE_QUERY = 3  # Corresponds to shortest imaginable query `a-a`.
        self.MULTIPLE_QUERIES = 50000  # Corresponds to a file containing 1000 queries.
        self.multiline_queries_with_none = None
        self.multiline_queries_without_none = "The Catcher in the Rye - J.D Salinger\nEternal Curse on the Reader of These Pages - Manual Puig\n"

    def test_read_file_should_raise_input_file_is_empty_exception_where_file_is_empty(
        self,
    ):
        with pytest.raises(InputFileIsEmpty):
            with patch("os.path.getsize", return_value=self.EMPTY_FILE):
                read_file(self.mock_path_to_file)

    def test_read_file_should_raise_file_not_found_error_where_file_is_not_found(
        self,
    ):
        with pytest.raises(FileNotFoundError):
            read_file(self.mock_path_to_file)

    def test_read_file_should_raise_print_custom_file_not_found_error_message_where_file_is_not_found(
        self,
    ):
        with pytest.raises(
            FileNotFoundError,
            match=f"Please check '{self.mock_path_to_file}' is a valid path",
        ):
            read_file(self.mock_path_to_file)

    def test_read_file_should_remove_queries_equal_to_none(self):
        with patch("os.path.getsize", return_value=self.SINGLE_QUERY):

            mock = mock_open(read_data=self.multiline_queries_with_none)
            with patch("src.common.app_io.reader.reader.codecs.open", mock):
                assert read_file(self.mock_path_to_file) == []

    def test_read_file_should_return_queries_where_no_queries_are_equal_to_none(
        self,
    ):
        with patch("os.path.getsize", return_value=self.SINGLE_QUERY):
            mock = mock_open(read_data=self.multiline_queries_without_none)
            with patch("src.common.app_io.reader.reader.codecs.open", mock):
                assert read_file(self.mock_path_to_file) == [
                    "The Catcher in the Rye - J.D Salinger",
                    "Eternal Curse on the Reader of These Pages - Manual Puig",
                ]
