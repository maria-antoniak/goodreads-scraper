import bs4

from src.book_id.result.result_model import ResultModel
from src.book_id.result.result_service import ResultService
from src.common.errors.errors import (return_none_for_index_error,
                                      return_none_for_type_error)


@return_none_for_type_error
@return_none_for_index_error
def build_result_models(results: [bs4.element.ResultSet]) -> [ResultModel]:
    result_models = []

    for result in results:

        result_service = ResultService(result)

        author_name = result_service._get_author_name(result)
        book_href = result_service._get_book_href(result)

        result_models.append(
            ResultModel(
                book_title=result_service._get_book_title(result),
                author_name=result_service._clean_author_name(author_name),
                book_id=result_service._get_id_from_href(book_href),
            )
        )

    return result_models
