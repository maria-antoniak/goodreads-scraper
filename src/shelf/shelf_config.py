from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("/home/studs/PycharmProjects/goodreads-scraper/config.ini")

# SHELF

config_number_of_shelf_results = config_object["BOOK"].getint("NUMBER_OF_SHELF_RESULTS")
