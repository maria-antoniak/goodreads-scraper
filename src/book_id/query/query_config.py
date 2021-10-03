from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("/home/studs/PycharmProjects/goodreads-scraper/config.ini")

# QUERY

config_delimiter = config_object["QUERY"].get("DELIMITER")
