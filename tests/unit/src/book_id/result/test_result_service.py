from data.no_result import no_result
from data.yoshimoto import yoshimoto_soup

from src.book_id.result.result_service import ResultService


class TestResultService:
    def setup_method(self):

        self.result_service = ResultService(yoshimoto_soup)
        self.result_service_empty = ResultService(no_result)

        self.href = "/book/show/50144.Kitchen?from_search=true&from_srp=true&qid=JBRJrWZAoO&rank=2"
        self.author_name_with_goodreads_author_parenthesis = (
            "Banana Yoshimoto (Goodreads Author)"
        )
        self.author_name_without_goodreads_author_parenthesis = "Banana Yoshimoto"

    def test_get_results_should_return_length_of_3(self):
        results = self.result_service.get_results()
        assert len(results) == 3

    def test_get_results_should_return_empty_list_where_soup_is_none(self):
        assert self.result_service_empty.get_results() == []

    def test_get_book_title_should_return_book_title_where_book_title_is_present(
        self,
    ):
        result = self.result_service.get_results()[1]
        assert self.result_service._get_book_title(result) == "Kitchen"

    def test_get_book_title_should_return_none_where_book_title_is_not_present(self):
        assert self.result_service_empty._get_book_title(None) is None

    def test_get_author_name_should_return_author_name_where_author_name_is_present(
        self,
    ):
        result = self.result_service.get_results()[1]
        assert self.result_service._get_author_name(result) == "Banana Yoshimoto"

    def test_get_author_name_should_return_none_where_author_name_is_not_present(
        self,
    ):
        assert self.result_service_empty._get_author_name(None) is None

    def test_clean_author_name_should_remove_goodreads_author_parenthesis_where_present(
        self,
    ):
        assert (
            self.result_service._clean_author_name(
                self.author_name_with_goodreads_author_parenthesis
            )
            == "Banana Yoshimoto"
        )

    def test_clean_author_name_should_return_goodreads_author_where_goodreads_author_parenthesis_is_not_present(
        self,
    ):
        assert (
            self.result_service._clean_author_name(
                self.author_name_without_goodreads_author_parenthesis
            )
            == "Banana Yoshimoto"
        )

    def test_clean_author_name_should_return_none_where_author_name_is_none(self):
        assert self.result_service_empty._clean_author_name(None) is None

    def test_get_book_href_should_return_book_href_where_book_href_is_present(self):
        result = self.result_service.get_results()[1]
        assert (
            self.result_service._get_book_href(result)
            == "/book/show/50144.Kitchen?from_search=true&from_srp=true&qid=JBRJrWZAoO&rank=2"
        )

    def test_get_book_href_should_return_none_where_book_href_is_not_present(self):
        result = self.result_service_empty.get_results()
        assert self.result_service_empty._get_book_href(result) is None

    def test_get_book_id_from_href_should_return_book_id_where_book_id_is_present_in_href(
        self,
    ):
        assert self.result_service._get_id_from_href(self.href) == "50144.Kitchen"

    def test_get_book_id_from_href_should_return_none_where_href_has_no_attribute_group(
        self,
    ):
        assert self.result_service_empty._get_id_from_href("") is None

    def test_get_book_id_from_href_should_return_none_where_href_is_none(self):
        assert self.result_service_empty._get_id_from_href(None) is None
