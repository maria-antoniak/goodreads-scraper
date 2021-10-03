from src.book_id.query.query_model import QueryModel
from src.book_id.query.query_service import QueryService


def build_query_model(query: str) -> QueryModel:

    query_service = QueryService(query)

    book_title = query_service._split_on_last_delimiter()[0]
    author_name = query_service._split_on_last_delimiter()[1]

    if query_service._is_subtitle_in_book_title(book_title):
        book_title_minus_subtitle = query_service._remove_subtitle_from_book_title(
            book_title
        )
    else:
        book_title_minus_subtitle = None

    return QueryModel(
        book_title=book_title,
        author_name=author_name,
        book_title_minus_subtitle=book_title_minus_subtitle,
        book_title_and_author_name_search_url=query_service._build_search_url_from_query(
            f"{book_title} - {author_name}"
        ),
        book_title_search_url=query_service._build_search_url_from_query(
            f"{book_title}"
        ),
        book_title_minus_subtitle_search_url=query_service._build_search_url_from_query(
            book_title_minus_subtitle
        ),
    )
