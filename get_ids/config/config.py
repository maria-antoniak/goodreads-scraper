from configparser import ConfigParser

config_object = ConfigParser()

config_object.read('config.ini')

# INPUT

path_to_input_file = config_object["INPUT"]["PATH_TO_INPUT_FILE"]

# DELIMITER

input_file_delimiter = config_object["DELIMITER"]["INPUT_FILE_DELIMITER"]

# OUTPUT

matches_directory_path = config_object["OUTPUT"]["MATCHES_DIRECTORY_PATH"]
matches_filename = config_object["OUTPUT"]["MATCHES_FILENAME"]

no_matches_directory_path = config_object["OUTPUT"]["NO_MATCHES_DIRECTORY_PATH"]
no_matches_filename = config_object["OUTPUT"]["NO_MATCHES_FILENAME"]

# MATCH_PERCENTAGES

book_title_similarity_percentage = float(
    config_object["MATCH_PERCENTAGES"]["BOOK_TITLE_SIMILARITY_PERCENTAGE"]
)
author_name_similarity_percentage = float(
    config_object["MATCH_PERCENTAGES"]["AUTHOR_NAME_SIMILARITY_PERCENTAGE"]
)
