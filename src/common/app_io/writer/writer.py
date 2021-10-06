import codecs
import json
import os
from typing import Dict, List, Union

import pandas as pd

from src.common.app_io.reader.reader import aggregate_books


def _is_directory_created(path_to_output_directory: str) -> bool:
    return os.path.isdir(path_to_output_directory)


def write_to_txt(path_to_output_directory: str, output_filename: str, book_id: str):
    with codecs.open(
        f"{path_to_output_directory}/{output_filename}.txt", "a", encoding="UTF-8"
    ) as SOURCE:
        return SOURCE.write(f"{book_id}\n")


def write_to_json(data: Union[Dict, List], _path: str):
    with open(_path, "w") as p:
        return json.dump(data, p, ensure_ascii=False, sort_keys=True, indent=4)


def write_to_csv(path_to_json_containing_all_books: str):
    book_df = pd.read_json(path_to_json_containing_all_books)
    return book_df.to_csv(
        f"{path_to_json_containing_all_books}.csv", index=False, encoding="utf-8"
    )


def create_export_file(args):
    books = aggregate_books(args.output_directory_path)
    all_books_json = f"{args.output_directory_path}/{'all_books.json'}"
    if args.format == "json":
        write_to_json(books, all_books_json)
    elif args.format == "csv":
        write_to_json(books, all_books_json)
        write_to_csv(all_books_json)
