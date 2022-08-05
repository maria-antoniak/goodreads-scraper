# TODO offer config option to infer `writingLanguages` from `countryOfCitizenship` if known

import sys

from SPARQLWrapper import JSON, SPARQLWrapper

from src.author.author_config import *
from src.author.author_model import AuthorModel
from src.author.author_service import AuthorService
from src.author.sparql_queries import author_details_query, search_query
from src.common.errors.errors import return_none_for_index_error
from src.common.utils.dict_operators import deep_get


def search_for_result(author_full_name: str):
    pass


endpoint_url = "https://query.wikidata.org/sparql"


def get_results(endpoint_url, query):

    vi1, vi2 = (
        sys.version_info[0],
        sys.version_info[1],
    )
    user_agent = f"WDQS-example Python/{vi1}.{vi2}"

    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


# TODO check encoding issues such as `Patrick Suskind`
# TODO check strange results for `Mikhail Lermontov`


@return_none_for_index_error
def build_author_model(author_name: str) -> AuthorModel:

    query = search_query.replace("QUERY", author_name)

    results = get_results(endpoint_url, query)["results"]["bindings"][0]
    code = deep_get(results, "item.value").rsplit("/", 1)[-1]

    author_query = author_details_query.replace("QUERY", code)

    author_details = get_results(endpoint_url, author_query)
    author_details_json = author_details["results"]["bindings"]

    author_service = AuthorService(author_details_json)

    author_model = AuthorModel(
        age_at_death=author_service._calculate_age_at_death(
            author_service.get_date_of_death(), author_service.get_date_of_birth()
        )
        if config_age_at_death is True
        else None,
        birth_full_name=author_service.get_birth_full_name()
        if config_birth_full_name is True
        else None,
        birth_full_name_in_native_language=author_service.get_birth_full_name_in_native_language()
        if config_birth_full_name_in_native_language is True
        else None,
        cause_of_death=author_service.get_cause_of_death()
        if config_cause_of_death is True
        else None,
        country_of_citizenship=author_service.get_country_of_citizenship()
        if config_country_of_citizenship is True
        else None,
        date_of_birth=author_service.get_date_of_birth()
        if config_date_of_birth is True
        else None,
        date_of_death=author_service.get_date_of_death()
        if config_date_of_death is True
        else None,
        educated_at=author_service.get_educated_at()
        if config_educated_at is True
        else None,
        gender=author_service.get_gender() if config_gender is True else None,
        genres=author_service.get_genres() if config_genres is True else None,
        lifestyle=author_service.get_lifestyle() if config_lifestyle is True else None,
        literary_movements=author_service.get_literary_movements()
        if config_literary_movements is True
        else None,
        manner_of_death=author_service.get_manner_of_death()
        if config_manner_of_death is True
        else None,
        native_language=author_service.get_native_language()
        if config_native_language is True
        else None,
        notable_works=author_service.get_notable_works()
        if config_notable_works is True
        else None,
        occupations=author_service.get_occupations()
        if config_occupations is True
        else None,
        place_of_birth=author_service.get_place_of_birth()
        if config_place_of_birth is True
        else None,
        place_of_burial=author_service.get_place_of_burial()
        if config_place_of_burial is True
        else None,
        place_of_death=author_service.get_place_of_death()
        if config_place_of_death is True
        else None,
        religion=author_service.get_religion() if config_religion is True else None,
        last_words=author_service.get_last_words()
        if config_last_words is True
        else None,
        work_period_start_year=author_service.get_work_period_start_year()
        if config_work_period_start_year is True
        else None,
        writing_languages=author_service.get_writing_languages()
        if config_writing_languages is True
        else None,
    )

    model = author_model
    return model
