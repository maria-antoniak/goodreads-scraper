# Call service that actually does the thing
import pprint
from typing import Dict

from src.author.author_config import *
from src.author.author_model import AuthorModel
from src.author.author_service import AuthorService

from src.common.formatters.json.to_json import to_json
from src.common.network.network import (_is_wikipedia_result_an_exact_match,
                                        get, search_for_wikipedia_result)
from src.common.parser.parser import parse
from src.common.utils.time_it import timeit

author_name = "Franz Kafka"

result = search_for_wikipedia_result(author_name)


if _is_wikipedia_result_an_exact_match(author_name, result):
    soup = parse(result.html())
    author_service = AuthorService(author_name, soup)


    date_of_birth = author_service.get_date_of_birth()
    city_of_birth = author_service.get_city_of_birth()
    country_of_birth = author_service.get_country_of_birth(city_of_birth)


    print(date_of_birth)
    print(city_of_birth)
    print(country_of_birth)