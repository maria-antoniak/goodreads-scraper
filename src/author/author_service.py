import re
import string
from typing import Dict, List, Optional

from dateutil import parser
from dateutil.relativedelta import relativedelta

from src.common.errors.errors import return_none_for_attribute_error
from src.common.utils.dict_operators import deep_get


class AuthorService:
    def __init__(self, author_details_json: [Dict]):

        self.author_details_json = author_details_json

    def _get_nested_result(self, key: str, first_result=True):
        results = list(
            set([deep_get(v, f"{key}.value") for v in self.author_details_json])
        )
        if first_result:
            return string.capwords(results[0])
        return [string.capwords(result) for result in results]

    @return_none_for_attribute_error
    def get_birth_full_name(self) -> Optional[str]:
        """
        P1477
        Example: `Doris Lessing` was born `Doris May Tayler`
        Or in the case of `Octavio Paz Lozano` where `Lozano` is dropped
        """
        return AuthorService._get_nested_result(self, "birthFullName")

    @return_none_for_attribute_error
    def get_birth_full_name_in_native_language(self) -> Optional[str]:
        #  P1559
        return AuthorService._get_nested_result(
            self, "birthFullNameInNativeLanguageLabel"
        )

    @return_none_for_attribute_error
    def get_cause_of_death(self) -> Optional[str]:
        #  P509
        return AuthorService._get_nested_result(self, "causeOfDeathLabel")

    @return_none_for_attribute_error
    def get_country_of_citizenship(self) -> Optional[str]:
        #  P27
        return AuthorService._get_nested_result(self, "countryOfCitizenshipLabel")

    @return_none_for_attribute_error
    def get_gender(self) -> Optional[str]:
        #  P21
        return AuthorService._get_nested_result(self, "genderLabel")

    @return_none_for_attribute_error
    def get_date_of_birth(self) -> Optional[str]:
        #  P569
        dob = AuthorService._get_nested_result(self, "dateOfBirthLabel")
        if dob:
            return dob.replace("t00:00:00z", "")
        return None

    @return_none_for_attribute_error
    def get_place_of_birth(self) -> Optional[str]:
        #  P19
        return AuthorService._get_nested_result(self, "placeOfBirthLabel")

    @return_none_for_attribute_error
    def get_date_of_death(self) -> Optional[str]:
        #  P570
        dod = AuthorService._get_nested_result(self, "dateOfDeathLabel")
        if dod:
            return dod.replace("t00:00:00z", "")
        return None

    @return_none_for_attribute_error
    def get_place_of_death(self) -> Optional[str]:
        #  P20
        return AuthorService._get_nested_result(self, "placeOfDeathLabel")

    @return_none_for_attribute_error
    def get_manner_of_death(self) -> Optional[str]:
        #  P1196
        return AuthorService._get_nested_result(self, "mannerOfDeathLabel")

    @staticmethod
    def _calculate_age_at_death(
        date_of_death: str, date_of_birth: str
    ) -> Optional[int]:

        if date_of_death:
            date_of_death_datetime_object = parser.parse(date_of_death).date()
            date_of_birth_datetime_object = parser.parse(date_of_birth).date()
            return relativedelta(
                date_of_death_datetime_object, date_of_birth_datetime_object
            ).years
        return None

    @return_none_for_attribute_error
    def get_age_at_death(self) -> Optional[str]:
        return AuthorService._get_nested_result(self, "ageAtDeathLabel")

    @return_none_for_attribute_error
    def get_place_of_burial(self) -> Optional[str]:
        #  P119
        return AuthorService._get_nested_result(self, "placeOfBurialLabel")

    @return_none_for_attribute_error
    def get_native_language(self) -> Optional[List[str]]:
        #  P103
        return AuthorService._get_nested_result(self, "writingLanguageLabel")

    @return_none_for_attribute_error
    def get_work_period_start_year(self) -> Optional[int]:
        #  P2031
        date = AuthorService._get_nested_result(self, "workPeriodStartLabel")
        if date:
            date_formatted = re.sub(
                r"-(?P<day>\d{2})-(?P<month>\d{2})(?P<time>t.+z)", "", date
            )
            return int(date_formatted)
        return None

    @return_none_for_attribute_error
    def get_writing_languages(self) -> Optional[List[str]]:
        #  P6886
        return AuthorService._get_nested_result(
            self, "writingLanguageLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_occupations(self) -> Optional[List[str]]:
        #  P106
        return sorted(
            AuthorService._get_nested_result(
                self, "occupationLabel", first_result=False
            )
        )

    @return_none_for_attribute_error
    def get_literary_movements(self) -> Optional[List[str]]:
        #  P135
        return AuthorService._get_nested_result(
            self, "literaryMovementLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_educated_at(self) -> Optional[List[str]]:
        #  P69
        return AuthorService._get_nested_result(
            self, "educatedAtLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_lifestyle(self) -> Optional[List[str]]:
        #  P1576
        return AuthorService._get_nested_result(
            self, "lifestyleLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_religion(self) -> Optional[str]:
        #  P140
        return AuthorService._get_nested_result(self, "religionLabel")

    @return_none_for_attribute_error
    def get_last_words(self) -> Optional[str]:
        #  P3909
        return AuthorService._get_nested_result(self, "lastWordsLabel")

    @return_none_for_attribute_error
    def get_notable_works(self) -> Optional[List[str]]:
        #  P800
        return sorted(
            AuthorService._get_nested_result(
                self, "notableWorksLabel", first_result=False
            )
        )

    @return_none_for_attribute_error
    def get_genres(self) -> Optional[List[str]]:
        #  P136
        return AuthorService._get_nested_result(self, "genreLabel", first_result=False)
