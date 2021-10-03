from data.empty import empty_soup
from data.yoshimoto import yoshimoto_soup

from src.book_id.result.result_controller import build_result_models
from src.book_id.result.result_model import ResultModel
from src.book_id.result.result_service import ResultService


class TestResultController:
    def setup_method(self):

        self.result_service = ResultService(yoshimoto_soup)
        self.results = self.result_service.get_results()

        self.empty_result_service = ResultService(empty_soup)
        self.empty_results = self.empty_result_service.get_results()

    def test_build_results_should_return_3_models(self):
        result_models = build_result_models(self.results)
        assert len(result_models) == 3

    def test_build_results_should_return_models_of_type_result_model(self):
        result_models = build_result_models(self.results)
        assert any(type(result_model) == ResultModel for result_model in result_models)

    def test_build_results_should_return_an_empty_list_where_results_is_none(self):
        result_models = build_result_models(self.empty_results)
        assert result_models == []
