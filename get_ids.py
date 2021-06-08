from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union


from get_ids.config.config import (author_name_similarity_percentage,
                           book_title_similarity_percentage,
                           input_file_delimiter, matches_directory_path,
                           matches_filename, no_matches_directory_path,
                           no_matches_filename, path_to_input_file)
from get_ids.models.query_model import QueryModel
from get_ids.models.result_model import ResultModel
from get_ids.network.network import get
from get_ids.parse.parser import parse_response
from get_ids.query.query_model_builder import build_query_model
from get_ids.reader.reader import read_file
from get_ids.result.result_match_handler import get_match
from get_ids.result.result_model_builder import build_result_models
from get_ids.result.result_parser import get_results
from get_ids.writer.writer import write_to_file

MAX_THREADS = 25


def match_handler(query_model: QueryModel) -> Union[ResultModel, QueryModel]:
    search_strategies = [
        query_model.book_title_and_author_name_search_url,
        query_model.book_title_search_url,
        query_model.book_title_minus_subtitle_search_url,
    ]

    for search_strategy in search_strategies:
        if search_strategy is not None:
            url = search_strategy
            response = get(url)
            soup = parse_response(response)
            result_models = build_result_models(get_results(soup))
            match = get_match(
                query_model,
                result_models,
                book_title_similarity_percentage,
                author_name_similarity_percentage,
            )

            if match:
                return match
    return query_model


if __name__ == "__main__":

    queries = read_file(path_to_input_file=path_to_input_file)
    query_models = [build_query_model(query, input_file_delimiter) for query in queries]

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = (
            executor.submit(match_handler, query_model) for query_model in query_models
        )
        for future in as_completed(futures):
            result = future.result()
            if isinstance(result, ResultModel):
                print(result.book_id)
                write_to_file(
                    path_to_output_directory=matches_directory_path,
                    output_filename=matches_filename,
                    book_id=result.book_id,
                )
            else:
                write_to_file(
                    path_to_output_directory=no_matches_directory_path,
                    output_filename=no_matches_filename,
                    book_id=f"{result.book_title}-{result.author_name}",
                )
