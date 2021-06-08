import pytest
from mock import mock_open, patch

from get_ids.writer.writer import _is_directory_created, write_to_file


class TestWriter:
    def setup_method(self):
        self.dummy_path = "this/is/a/dummy/path"

    def test_ut_write_file_should_write_book_id_to_empty_file(self):
        open_mock = mock_open()
        with patch("get_ids.writer.writer.codecs.open", open_mock, create=True):
            write_to_file("/output", "results", "160653.Actual_Air")

        open_mock.assert_called_with("/output/results.txt", "a", encoding="UTF-8")
        open_mock.return_value.write.assert_called_once_with("160653.Actual_Air\n")

    def test_ut_write_file_should_raise_file_not_found_error_where_path_to_write_is_invalid(
        self,
    ):
        with pytest.raises(FileNotFoundError):
            write_to_file("/output", "results", "160653.Actual_Air")

    def test_ut_write_file_should_true_for_existing_directory(self):
        with patch("os.path.isdir") as mock:
            mock.return_value = False
            assert _is_directory_created(self.dummy_path) is False

    def test_ut_write_file_should_false_for_non_existent_directory(self):
        with patch("os.path.isdir") as mock:
            mock.return_value = True
            assert _is_directory_created(self.dummy_path) is True
