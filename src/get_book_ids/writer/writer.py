import codecs
import os


def _is_directory_created(path_to_output_directory: str) -> bool:
    return os.path.isdir(path_to_output_directory)


def write_to_file(path_to_output_directory: str, output_filename: str, book_id: str):
    with codecs.open(
        f"{path_to_output_directory}/{output_filename}.txt", "a", encoding="UTF-8"
    ) as SOURCE:
        return SOURCE.write(f"{book_id}\n")
