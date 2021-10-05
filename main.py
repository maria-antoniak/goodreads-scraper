import argparse
import json
import logging
from typing import Dict

import pandas as pd

from src.book.book_controller import build_book_model
from src.book_id.book_id_controller import run

from src.common.app_io.reader.reader import (condense_books,
                                             get_books_already_scraped,
                                             get_books_to_scrape, read_file)

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)


def generate_json(data: Dict, _path: str):
    with open(_path, "w") as p:
        return json.dump(data, p, ensure_ascii=False, sort_keys=True, indent=4)


def generate_csv(path_to_json_containing_all_books: str):
    book_df = pd.read_json(path_to_json_containing_all_books)
    return book_df.to_csv(f"{path_to_json_containing_all_books}.csv", index=False, encoding="utf-8")


def manage_user_specified_format(args):
    books = condense_books(args.output_directory_path)
    condensed_books_path = f"{args.output_directory_path}/{'all_books.json'}"
    if args.format == "json":
        generate_json(books, condensed_books_path)
    elif args.format == "csv":
        generate_json(books, condensed_books_path)
        generate_csv(condensed_books_path)


def main():

    parser = argparse.ArgumentParser()

    # BOOK SERVICE

    parser.add_argument("-s", "--service", type=str, choices=["book", "book_id"])
    parser.add_argument("-bip", "--book_ids_path", type=str)
    parser.add_argument("-odp", "--output_directory_path", type=str)
    parser.add_argument(
        "-f", "--format", type=str, default="json", choices=["json", "csv"]
    )

    args = parser.parse_args()

    if args.service == "book":

        ids = read_file(args.book_ids_path)

        books_already_scraped = get_books_already_scraped(args.output_directory_path)
        books_ids_to_scrape = get_books_to_scrape(ids, books_already_scraped)

        for book_id in books_ids_to_scrape:

            book_model = build_book_model(book_id)
            path = f"{args.output_directory_path}/{book_id}.json"
            generate_json(book_model, path)

        manage_user_specified_format(args)
        logging.info("🎉 Success! All book metadata scraped. 🎉")

    if args.service == "book_id":
        run()


if __name__ == "__main__":
    main()
