from difflib import SequenceMatcher

from src.book_id.query.query_model import QueryModel
from src.book_id.result.result_model import ResultModel


def _is_results_equal_to_one(result_models: [ResultModel]) -> True:
    """Where a single result is returned for a query, we can assume it is correct."""
    if len(result_models) == 1:
        return True
    return False


def _is_input_similar(a: str, b: str, similarity_percentage: float) -> bool:
    """
    1.0 == Exact match
    0.0 is most permissive
    0.99 is least permissiveness
    """
    seq = SequenceMatcher(a=a, b=b)
    if seq.ratio() >= similarity_percentage:
        return True
    return False


def get_match(
    query_model: QueryModel,
    result_models: [ResultModel],
    book_title_similarity_percentage: float,
    author_name_similarity_percentage: float,
) -> [ResultModel, None]:
    if result_models:
        result_models = result_models[:]

        try:
            while len(result_models) != 0:
                for result_model in result_models:

                    book_title_match = _is_input_similar(
                        query_model.book_title,
                        result_model.book_title,
                        book_title_similarity_percentage,
                    )
                    author_name_match = _is_input_similar(
                        query_model.author_name,
                        result_model.author_name,
                        author_name_similarity_percentage,
                    )

                    if book_title_match and author_name_match:
                        return result_model
                    result_models.remove(result_model)
            return None
        except ValueError:
            return None
    else:
        return None
