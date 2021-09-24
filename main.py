import argparse
from enum import Enum

from src.book.controller.book_controller import build_book_model
from src.common.app_io.reader.reader import read_file


class Service(Enum):
    BOOK = build_book_model


def main():

    parser = argparse.ArgumentParser()

    # BOOK SERVICE

    parser.add_argument("-s", "--service", type=str)
    parser.add_argument("-bip", "--book_ids_path", type=str)
    parser.add_argument("-odp", "--output_directory_path", type=str)

    args = parser.parse_args()

    book_ids = read_file(args.book_ids_path)

    if args.service == "book":
        for book_id in book_ids:
            build_book_model(book_id)


if __name__ == "__main__":
    main()
