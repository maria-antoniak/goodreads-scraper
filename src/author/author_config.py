from configparser import ConfigParser

config_object = ConfigParser()

config_object.read("/home/studs/PycharmProjects/goodreads-scraper/config.ini")

# BOOK

config_age_at_death = config_object["AUTHOR"].getboolean("AGE_AT_DEATH")
config_birth_full_name = config_object["AUTHOR"].getboolean("BIRTH_FULL_NAME")
config_birth_full_name_in_native_language = config_object["AUTHOR"].getboolean(
    "BIRTH_FULL_NAME_IN_NATIVE_LANGUAGE"
)
config_cause_of_death = config_object["AUTHOR"].getboolean("CAUSE_OF_DEATH")
config_country_of_citizenship = config_object["AUTHOR"].getboolean(
    "COUNTRY_OF_CITIZENSHIP"
)
config_date_of_birth = config_object["AUTHOR"].getboolean("DATE_OF_BIRTH")
config_date_of_death = config_object["AUTHOR"].getboolean("DATE_OF_DEATH")
config_educated_at = config_object["AUTHOR"].getboolean("EDUCATED_AT")
config_gender = config_object["AUTHOR"].getboolean("GENDER")
config_genres = config_object["AUTHOR"].getboolean("GENRES")
config_last_words = config_object["AUTHOR"].getboolean("LAST_WORDS")
config_lifestyle = config_object["AUTHOR"].getboolean("LIFESTYLE")
config_literary_movements = config_object["AUTHOR"].getboolean("LITERARY_MOVEMENTS")
config_manner_of_death = config_object["AUTHOR"].getboolean("MANNER_OF_DEATH")
config_native_language = config_object["AUTHOR"].getboolean("NATIVE_LANGUAGE")
config_notable_works = config_object["AUTHOR"].getboolean("NOTABLE_WORKS")
config_occupations = config_object["AUTHOR"].getboolean("OCCUPATIONS")
config_place_of_birth = config_object["AUTHOR"].getboolean("PLACE_OF_BIRTH")
config_place_of_burial = config_object["AUTHOR"].getboolean("PLACE_OF_BURIAL")
config_place_of_death = config_object["AUTHOR"].getboolean("PLACE_OF_DEATH")
config_religion = config_object["AUTHOR"].getboolean("RELIGION")
config_work_period_start_year = config_object["AUTHOR"].getboolean(
    "WORK_PERIOD_START_YEAR"
)
config_writing_languages = config_object["AUTHOR"].getboolean("WRITING_LANGUAGES")
