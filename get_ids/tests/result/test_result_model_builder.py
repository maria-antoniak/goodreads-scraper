from data.yoshimoto import yoshimoto_soup

from get_ids.models.result_model import ResultModel
from get_ids.result.result_model_builder import build_result_models
from get_ids.result.result_parser import get_results


class TestResultParser:
    def setup_method(self):
        #  It would be better to mock bs4.element.ResultSet here.
        self.results = get_results(yoshimoto_soup)

    def test_it_build_results_should_return_3_models(self):
        result_models = build_result_models(self.results)
        assert len(result_models) == 3

    def test_it_build_results_should_return_models_of_type_result_model(self):
        result_models = build_result_models(self.results)
        assert any(type(result_model) == ResultModel for result_model in result_models)

    def test_it_build_results_should_return_none_where_results_is_none(self):
        result_models = build_result_models(None)
        assert result_models is None
