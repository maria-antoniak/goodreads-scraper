import bs4

from get_ids.errors.errors import return_none_for_type_error
from get_ids.models.result_model import ResultModel
from get_ids.result.result_parser import (_clean_author_name, _get_author_name,
                                  _get_book_href, _get_book_title,
                                  _get_id_from_href)


@return_none_for_type_error
def build_result_models(results: [bs4.element.ResultSet]) -> [ResultModel]:
    result_models = []

    for result in results:

        author_name = _get_author_name(result)

        result_models.append(
            ResultModel(
                book_title=_get_book_title(result),
                author_name=_clean_author_name(author_name),
                book_id=_get_id_from_href(_get_book_href(result)),
            )
        )

    return result_models
