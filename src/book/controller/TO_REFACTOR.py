# import argparse
# import json
# import os
# import re
# import time
# from datetime import datetime
# from urllib.error import HTTPError
#
# from .get_book_controller import scrape_book
#
# import bs4
# import pandas as pd
#
#
# def get_book_ids(book_ids_path: str) -> [str]:
#     return [line.strip() for line in open(book_ids_path, "r") if line]
#
#
# def get_books_already_scraped(output_directory_path: str) -> [str]:
#     return [
#         file_name.replace(".json", "")
#         for file_name in os.listdir(output_directory_path)
#         if file_name.endswith(".json") and not file_name.startswith("all_books")
#     ]
#
#
# def get_books_to_scrape(book_ids: [str], books_already_scraped: [str]) -> [str]:
#     return list(set(book_ids) - set(books_already_scraped))
#
#
# def condense_books(books_directory_path):
#
#     books = []
#
#     for file_name in os.listdir(books_directory_path):
#         if (
#             file_name.endswith(".json")
#             and not file_name.startswith(".")
#             and file_name != "all_books.json"
#         ):
#             _book = json.load(
#                 open(books_directory_path + "/" + file_name, "r")
#             )  # , encoding='utf-8', errors='ignore'))
#             books.append(_book)
#
#     return books
#
#
#
#
#
# def main():
#
#     start_time = datetime.now()
#     script_name = os.path.basename(__file__)
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--book_ids_path", type=str)
#     parser.add_argument("--output_directory_path", type=str)
#     parser.add_argument(
#         "--format",
#         type=str,
#         action="store",
#         default="json",
#         dest="format",
#         choices=["json", "csv"],
#         help="set file output format",
#     )
#     args = parser.parse_args()
#
#     book_ids = get_book_ids(args.book_ids_path)
#     books_already_scraped = get_books_already_scraped(args.output_directory_path)
#     books_to_scrape = get_books_to_scrape(book_ids, books_already_scraped)
#     condensed_books_path = f"{args.output_directory_path}/{'all_books'}"
#
#     for index, book_id in enumerate(books_to_scrape):
#         try:
#             print(
#                 str(datetime.now())
#                 + " "
#                 + script_name
#                 + ": Scraping "
#                 + book_id
#                 + "..."
#             )
#             print(
#                 str(datetime.now())
#                 + " "
#                 + script_name
#                 + ": #"
#                 + str(index + 1 + len(books_already_scraped))
#                 + " out of "
#                 + str(len(book_ids))
#                 + " books"
#             )
#
#             book = scrape_book(book_id)
#             json.dump(
#                 book, open(args.output_directory_path + "/" + book_id + ".json", "w")
#             )
#
#             print("=============================")
#
#         except HTTPError as e:
#             print(e)
#             exit(0)
#
#     books = condense_books(args.output_directory_path)
#     if args.format == "json":
#         json.dump(books, open(f"{condensed_books_path}.json", "w"))
#     elif args.format == "csv":
#         json.dump(books, open(f"{condensed_books_path}.json", "w"))
#         book_df = pd.read_json(f"{condensed_books_path}.json")
#         book_df.to_csv(f"{condensed_books_path}.csv", index=False, encoding="utf-8")
#
#     print(
#         str(datetime.now())
#         + " "
#         + script_name
#         + f":\n\n🎉 Success! All book metadata scraped. 🎉\n\nMetadata files have been output to /{args.output_directory_path}\nGoodreads scraping run time = ⏰ "
#         + str(datetime.now() - start_time)
#         + " ⏰"
#     )
#
#
# if __name__ == "__main__":
#     main()
