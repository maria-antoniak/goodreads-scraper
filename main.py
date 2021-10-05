import argparse
import json
import logging
from typing import Dict

import pandas as pd

from src.book.book_controller import build_book_model
from src.common.app_io.reader.reader import (condense_books,
                                             get_books_already_scraped,
                                             get_books_to_scrape, read_file)

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)


def generate_json(data: Dict, _path: str):
    with open(_path, "w") as p:
        return json.dump(data, p, ensure_ascii=False, sort_keys=True, indent=4)


def main():

    parser = argparse.ArgumentParser()

    # BOOK SERVICE

    parser.add_argument("-s", "--service", type=str, choices=["book"])
    parser.add_argument("-bip", "--book_ids_path", type=str)
    parser.add_argument("-odp", "--output_directory_path", type=str)
    parser.add_argument(
        "-f", "--format", type=str, default="json", choices=["json", "csv"]
    )

    args = parser.parse_args()

    if args.service == "book":

        book_ids = read_file(args.book_ids_path)

        books_already_scraped = get_books_already_scraped(args.output_directory_path)
        books_ids_to_scrape = get_books_to_scrape(book_ids, books_already_scraped)

        for book_id in books_ids_to_scrape:

            book_model = build_book_model(book_id)
            path = f"{args.output_directory_path}/{book_id}.json"
            generate_json(book_model, path)

        books = condense_books(args.output_directory_path)
        condensed_books_path = f"{args.output_directory_path}/{'all_books.json'}"

        if args.format == "json":
            generate_json(books, condensed_books_path)
        elif args.format == "csv":
            generate_json(books, condensed_books_path)
            book_df = pd.read_json(condensed_books_path)
            book_df.to_csv(f"{condensed_books_path}.csv", index=False, encoding="utf-8")

        logging.info("🎉 Success! All book metadata scraped. 🎉")


        # if args.service == "book":
        #    list(map(build_book_model, book_ids))
        #
        # if args.service == "book_id":
        #    pass
        #    # list(map(build_book_model, book_ids))


if __name__ == "__main__":
    main()
