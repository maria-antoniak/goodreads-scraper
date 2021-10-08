import pprint
import sys
from typing import Dict

from SPARQLWrapper import JSON, SPARQLWrapper
from src.author.author_model import AuthorModel
from src.author.author_service import AuthorService
from src.common.formatters.json.to_json import to_json
from src.common.utils.dict_operators import deep_get

sparql_search_query = """

SELECT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q5;
    ?label "QUERY"@en.
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P106 ?statement1.
      ?statement1 (ps:P106/(wdt:P279*)) wd:Q36180.
    }
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 10

"""


sparql_author_details_query = """

SELECT DISTINCT ?item ?itemLabel ?gender ?genderLabel ?countryOfCitizenship ?countryOfCitizenshipLabel ?birthFullName ?birthFullNameLabel ?dateOfBirth ?dateOfBirthLabel ?dateOfDeath ?dateOfDeathLabel ?nativeLanguage ?nativeLanguageLabel ?writingLanguage ?writingLanguageLabel ?occupation ?occupationLabel ?literaryMovement ?literaryMovementLabel ?lifestyle ?lifestyleLabel ?religion ?religionLabel ?notableWorks ?notableWorksLabel ?genre ?genreLabel WHERE {
  VALUES ?item {
    wd:QUERY
  }
  OPTIONAL { ?item wdt:P21 ?gender. }
  OPTIONAL { ?item wdt:P27 ?countryOfCitizenship. }
  OPTIONAL { ?item wdt:P1477 ?birthFullName. }
  OPTIONAL { ?item wdt:P569 ?dateOfBirth. }
  OPTIONAL { ?item wdt:P570 ?dateOfDeath. }
  OPTIONAL { ?item wdt:P103 ?nativeLanguage. }
  OPTIONAL { ?item wdt:P6886 ?writingLanguage. }
  OPTIONAL { ?item wdt:P106 ?occupation. }
  OPTIONAL { ?item wdt:P135 ?literaryMovement. }
  OPTIONAL { ?item wdt:P1576 ?lifestyle. }
  OPTIONAL { ?item wdt:P140 ?religion. }
  OPTIONAL { ?item wdt:P800 ?notableWorks. }
  OPTIONAL { ?item wdt:P136 ?genre. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}

"""


def search_for_result(author_full_name: str):
    pass


endpoint_url = "https://query.wikidata.org/sparql"


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (
        sys.version_info[0],
        sys.version_info[1],
    )
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


query = sparql_search_query.replace("QUERY", "Franz Kafka")


results = get_results(endpoint_url, query)["results"]["bindings"][0]
code = deep_get(results, "item.value").rsplit("/", 1)[-1]
print(code)

author_query = sparql_author_details_query.replace("QUERY", code)


author_details = get_results(endpoint_url, author_query)
#  TODO Iterate over results to get a complete profile of author
# print(author_details['results']['bindings'])
author_details_json = author_details["results"]["bindings"]

# Testing

notable_works = set()
writing_language = set()
occupations = set()
literary_movement = set()

for json in author_details_json:
    author_service = AuthorService(json)
    notable_works.add(author_service.get_notable_works())
    writing_language.add(author_service.get_writing_language())
    occupations.add(author_service.get_occupation())
    literary_movement.add(author_service.get_literary_movement())

print(list(notable_works))
print(list(writing_language))
print(list(occupations))
print(list(literary_movement))


# def build_author_model(json: Dict) -> Dict:
#
#     author_service = AuthorService(json)
#
#     author_model = AuthorModel(
#         age_at_death=author_service._calculate_age_at_death(
#             author_service.get_date_of_death(), author_service.get_date_of_birth()
#         ),
#         birth_full_name=author_service.get_birth_full_name(),
#         birth_full_name_in_native_language=author_service.get_birth_full_name_in_native_language(),
#         cause_of_death=author_service.get_cause_of_death(),
#         country_of_citizenship=author_service.get_country_of_citizenship(),
#         date_of_birth=author_service.get_date_of_birth(),
#         date_of_death=author_service.get_date_of_death(),
#         educated_at=author_service.get_educated_at(),
#         gender=author_service.get_gender(),
#         genre=author_service.get_genre(),
#         lifestyle=author_service.get_lifestyle(),
#         literary_movement=author_service.get_literary_movement(),
#         manner_of_death=author_service.get_manner_of_death(),
#         native_language=author_service.get_native_language(),
#         notable_works=author_service.get_notable_works(),
#         occupation=author_service.get_occupation(),
#         place_of_birth=author_service.get_place_of_birth(),
#         place_of_burial=author_service.get_place_of_burial(),
#         place_of_death=author_service.get_place_of_death(),
#         religion=author_service.get_religion(),
#         writing_language=author_service.get_writing_language(),
#     )
#
#     model = author_model
#     result = to_json(model)
#     return result
#
#
# pprint.pprint(build_author_model(author_details_json))
