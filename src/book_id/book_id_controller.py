import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union

from src.book_id.book_id_config import *
from src.book_id.query.query_controller import build_query_model
from src.book_id.query.query_model import QueryModel
from src.book_id.result.match_service import get_match
from src.book_id.result.result_controller import build_result_models
from src.book_id.result.result_model import ResultModel
from src.book_id.result.result_service import ResultService
from src.common.app_io.reader.reader import read_file
from src.common.app_io.writer.writer import write_to_txt
from src.common.network.network import get
from src.common.parser.parser import parse

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

            response = get([url])
            soup = parse(response[0])

            result_service = ResultService(soup)
            results = result_service.get_results()
            result_models = build_result_models(results)

            match = get_match(
                query_model,
                result_models,
                config_book_title_similarity_percentage,
                config_author_name_similarity_percentage,
            )

            if match:
                return match
    return query_model


def run():

    queries = read_file(path_to_input_file=config_path_to_input_file)
    query_models = [build_query_model(query) for query in queries]

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = (
            executor.submit(match_handler, query_model) for query_model in query_models
        )
        for future in as_completed(futures):
            result = future.result()

            if isinstance(result, ResultModel):
                logging.info(f"|✔| '{result.book_id}'")
                write_to_txt(
                    path_to_output_directory=config_matches_directory_path,
                    output_filename=config_matches_filename,
                    book_id=result.book_id,
                )
            else:
                logging.info(f"|✕| '{result.book_title} - {result.author_name}'")
                write_to_txt(
                    path_to_output_directory=config_no_matches_directory_path,
                    output_filename=config_no_matches_filename,
                    book_id=f"{result.book_title} - {result.author_name}",
                )
