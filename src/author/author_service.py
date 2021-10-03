from typing import Dict, Union

from dateutil import parser
from dateutil.relativedelta import relativedelta


class AuthorService:
    def __init__(self, json: Dict):

        self.json = json

    def get_gender(self) -> Union[str, None]:
        #  P21
        pass

    def get_country_of_citizenship(self) -> Union[str, None]:
        #  P27
        pass

    def get_birth_full_name_in_native_language(self) -> Union[str, None]:
        #  P1559
        pass

    def get_birth_full_name(self) -> Union[str, None]:
        """
        P1477
        Example: `Doris Lessing` was born `Doris May Tayler`
        Or in the case of `Octavio Paz Lozano` where `Lozano` is dropped
        """
        pass

    def get_date_of_birth(self) -> Union[str, None]:
        #  P569
        pass

    def get_place_of_birth(self) -> Union[str, None]:
        #  P19
        pass

    def get_date_of_death(self) -> Union[str, None]:
        #  P570
        pass

    def get_place_of_death(self) -> Union[str, None]:
        #  P20
        pass

    def get_manner_of_death(self) -> Union[str, None]:
        #  P1196
        pass

    @staticmethod
    def get_cause_of_death(self) -> Union[str, None]:
        #  P509
        pass

    @staticmethod
    def _calculate_age_at_death(date_of_death: str, date_of_birth: str) -> int:
        date_of_death_datetime_object = parser.parse(date_of_death).date()
        date_of_birth_datetime_object = parser.parse(date_of_birth).date()
        return relativedelta(
            date_of_death_datetime_object, date_of_birth_datetime_object
        ).years

    @staticmethod
    def get_age_at_death() -> Union[int, None]:
        pass

    @staticmethod
    def get_place_of_burial() -> Union[str, None]:
        #  P119
        pass

    @staticmethod
    def get_native_language() -> Union[str, None]:
        #  P103
        pass

    @staticmethod
    def get_writing_language() -> Union[str, None]:
        #  P6886
        pass

    @staticmethod
    def get_occupation() -> Union[str, None]:
        #  P106
        pass

    @staticmethod
    def get_literary_movement() -> Union[str, None]:
        #  P135
        pass

    @staticmethod
    def get_educated_at() -> Union[str, None]:
        #  P69
        pass

    @staticmethod
    def get_lifestyle() -> Union[str, None]:
        #  P1576
        pass

    @staticmethod
    def get_religion() -> Union[str, None]:
        #  P140
        pass

    @staticmethod
    def get_last_words() -> Union[str, None]:
        #  P1455
        pass

    @staticmethod
    def get_notable_works() -> Union[Dict, None]:
        #  P800
        pass

    @staticmethod
    def get_genre() -> Union[str, None]:
        #  P136
        pass


"""

SELECT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q5.
  ?item ?label "Doris Lessing"@en .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} LIMIT 10


"""

"""
SELECT DISTINCT

?item ?itemLabel 
?gender ?genderLabel 
?countryOfCitizenship ?countryOfCitizenshipLabel
?birthFullName ?birthFullNameLabel
?dateOfBirth ?dateOfBirthLabel
?dateOfDeath ?dateOfDeathLabel
?nativeLanguage ?nativeLanguageLabel
?writingLanguage ?writingLanguageLabel
?occupation ?occupationLabel
?literaryMovement ?literaryMovementLabel
?lifestyle ?lifestyleLabel
?religion ?religionLabel
?notableWorks ?notableWorksLabel
?genre ?genreLabel
{

  VALUES (?item) { (wd:Q905) }
  
  
OPTIONAL { ?item wdt:P21 ?gender . }
OPTIONAL { ?item wdt:P27 ?countryOfCitizenship . }
OPTIONAL { ?item wdt:P1477 ?birthFullName . }
OPTIONAL { ?item wdt:P569 ?dateOfBirth . }
OPTIONAL { ?item wdt:P570 ?dateOfDeath . }
OPTIONAL { ?item wdt:P103 ?nativeLanguage . }
OPTIONAL { ?item wdt:P6886 ?writingLanguage . }
OPTIONAL { ?item wdt:P106 ?occupation . }
OPTIONAL { ?item wdt:P135 ?literaryMovement . }
OPTIONAL { ?item wdt:P1576 ?lifestyle . }
OPTIONAL { ?item wdt:P140 ?religion . }
OPTIONAL { ?item wdt:P800 ?notableWorks . }
OPTIONAL { ?item wdt:P136 ?genre . }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

}


"""
