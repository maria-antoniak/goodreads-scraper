from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("config.ini")

# INPUT

config_path_to_input_file = config_object["INPUT"].get("PATH_TO_INPUT_FILE")

# DELIMITER

config_delimiter = config_object["QUERY"].get("DELIMITER")

# OUTPUT

config_matches_directory_path = config_object["OUTPUT"]["MATCHES_DIRECTORY_PATH"]
config_matches_filename = config_object["OUTPUT"]["MATCHES_FILENAME"]

config_no_matches_directory_path = config_object["OUTPUT"]["NO_MATCHES_DIRECTORY_PATH"]
config_no_matches_filename = config_object["OUTPUT"]["NO_MATCHES_FILENAME"]

# MATCH_PERCENTAGES

config_book_title_similarity_percentage = float(
    config_object["MATCH_PERCENTAGES"]["BOOK_TITLE_SIMILARITY_PERCENTAGE"]
)
config_author_name_similarity_percentage = float(
    config_object["MATCH_PERCENTAGES"]["AUTHOR_NAME_SIMILARITY_PERCENTAGE"]
)
