import argparse

from src.book.book_controller import build_book_model
from src.common.app_io.reader.reader import read_file


def main():

    parser = argparse.ArgumentParser()

    # BOOK SERVICE

    parser.add_argument("-s", "--service", type=str)
    parser.add_argument("-bip", "--book_ids_path", type=str)
    parser.add_argument("-odp", "--output_directory_path", type=str)

    args = parser.parse_args()

    book_ids = read_file(args.book_ids_path)

    if args.service == "book":
        list(map(build_book_model, book_ids))

    if args.service == "book_id":
        pass
        # list(map(build_book_model, book_ids))


if __name__ == "__main__":
    main()
