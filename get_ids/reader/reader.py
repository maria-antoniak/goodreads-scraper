import codecs
import os

from get_ids.reader.exceptions import InputFileIsEmpty


def _get_queries_from_input_file(path_to_input_file: str) -> [str]:
    with codecs.open(path_to_input_file, "r", encoding="UTF-8") as SOURCE:
        return [line.strip() for line in SOURCE]


def _is_file_empty(path_to_input_file: str) -> bool:
    if os.path.getsize(path_to_input_file) == 0:
        return True
    return False


def _is_query_equal_to_none_present_in_queries(queries: list) -> bool:
    if None in queries:
        return True
    return False


def _filter_queries_equal_to_none(queries: list) -> list:
    return list(filter(None, [query for query in queries]))


def read_file(path_to_input_file: str) -> [str]:
    try:
        if _is_file_empty(path_to_input_file):
            raise InputFileIsEmpty(path_to_input_file)

        queries = _get_queries_from_input_file(path_to_input_file)

        if _is_query_equal_to_none_present_in_queries(queries):
            return _filter_queries_equal_to_none(queries)
        return queries

    except FileNotFoundError:
        raise FileNotFoundError(f"Please check '{path_to_input_file}' is a valid path")
