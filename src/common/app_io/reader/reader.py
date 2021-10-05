import codecs
import json
import os
from pathlib import Path
from typing import Dict

from src.common.app_io.reader.exceptions import InputFileIsEmpty


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


def _is_file_empty(path_to_input_file: str) -> bool:
    if os.path.getsize(path_to_input_file) == 0:
        return True
    return False


def _get_queries_from_input_file(path_to_input_file: str) -> [str]:
    with codecs.open(path_to_input_file, "r", encoding="UTF-8") as SOURCE:
        return [line.strip() for line in SOURCE]


def _is_query_equal_to_none_present_in_queries(queries: list) -> bool:
    if None in queries:
        return True
    return False


def _filter_queries_equal_to_none(queries: list) -> list:
    return list(filter(None, [query for query in queries]))


def get_books_already_scraped(output_directory_path: str) -> [str]:
    return [
        f.stem
        for f in Path(output_directory_path).rglob("*.json")
        if not f.stem.startswith("all_books")
    ]


def get_books_to_scrape(book_ids: [str], books_already_scraped: [str]) -> [str]:
    return list(set(book_ids) - set(books_already_scraped))


def _is_file_valid(file_name: str):
    if (
        file_name.endswith(".json")
        and not file_name.startswith(".")
        and file_name != "all_books.json"
    ):
        return True
    return False


def aggregate_books(output_directory_path: str) -> [Dict]:
    books = []
    valid = filter(_is_file_valid, os.listdir(output_directory_path))
    paths = [f"{output_directory_path}/{f}" for f in valid]

    for path in paths:
        f = json.load(open(path))
        books.append(f)
    return books
