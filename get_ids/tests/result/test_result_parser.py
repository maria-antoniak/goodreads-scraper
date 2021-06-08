from data.no_result import no_result
from data.yoshimoto import yoshimoto_soup

from get_ids.result.result_parser import (_clean_author_name, _get_author_name,
                                  _get_book_href, _get_book_title,
                                  _get_id_from_href, get_results)


class TestResultParser:
    def setup_method(self):
        #  It would be better to mock bs4.element.ResultSet here.
        self.results = get_results(yoshimoto_soup)
        self.href = "/book/show/50144.Kitchen?from_search=true&from_srp=true&qid=JBRJrWZAoO&rank=2"
        self.author_name_with_goodreads_author_parenthesis = (
            "Banana Yoshimoto (Goodreads Author)"
        )
        self.author_name_without_goodreads_author_parenthesis = "Banana Yoshimoto"

    def test_ut_get_results_should_return_length_of_3(self):
        results = get_results(yoshimoto_soup)
        assert len(results) == 3

    def test_ut_get_results_should_return_none_where_soup_is_none(self):
        assert get_results(None) is None

    def test_ut_get_book_title_should_return_book_title_where_book_title_is_present(
        self,
    ):
        result = self.results[1]
        assert _get_book_title(result) == "Kitchen"

    def test_ut_get_book_title_should_return_none_where_book_title_is_not_present(self):
        assert _get_book_title(no_result) is None

    def test_ut_get_author_name_should_return_author_name_where_author_name_is_present(
        self,
    ):
        result = self.results[1]
        assert _get_author_name(result) == "Banana Yoshimoto"

    def test_ut_get_author_name_should_return_none_where_author_name_is_not_present(
        self,
    ):
        assert _get_author_name(no_result) is None

    def test_ut_clean_author_name_should_remove_goodreads_author_parenthesis_where_present(
        self,
    ):
        assert (
            _clean_author_name(self.author_name_with_goodreads_author_parenthesis)
            == "Banana Yoshimoto"
        )

    def test_ut_clean_author_name_should_return_goodreads_author_where_goodreads_author_parenthesis_is_not_present(
        self,
    ):
        assert (
            _clean_author_name(self.author_name_without_goodreads_author_parenthesis)
            == "Banana Yoshimoto"
        )

    def test_ut_clean_author_name_should_return_none_where_author_name_is_none(self):
        assert _clean_author_name(None) is None

    def test_ut_get_book_href_should_return_book_href_where_book_href_is_present(self):
        result = self.results[1]
        assert (
            _get_book_href(result)
            == "/book/show/50144.Kitchen?from_search=true&from_srp=true&qid=JBRJrWZAoO&rank=2"
        )

    def test_ut_get_book_href_should_return_none_where_book_href_is_not_present(self):
        assert _get_book_href(no_result) is None

    def test_ut_get_book_id_from_href_should_return_book_id_where_book_id_is_present_in_href(
        self,
    ):
        assert _get_id_from_href(self.href) == "50144.Kitchen"

    def test_ut_get_book_id_from_href_should_return_none_where_href_has_no_attribute_group(
        self,
    ):
        assert _get_id_from_href("") is None

    def test_ut_get_book_id_from_href_should_return_none_where_href_is_none(self):
        assert _get_id_from_href(None) is None
