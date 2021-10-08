from typing import Dict, Union, List

from dateutil import parser
from dateutil.relativedelta import relativedelta
from src.common.utils.dict_operators import deep_get


class AuthorService:
    def __init__(self, json: Dict):

        self.json = json

    def get_gender(self) -> Union[str, None]:
        #  P21
        return deep_get(self.json, "genderLabel.value")

    def get_country_of_citizenship(self) -> Union[str, None]:
        #  P27
        return deep_get(self.json, "countryOfCitizenshipLabel.value")

    def get_birth_full_name_in_native_language(self) -> Union[str, None]:
        #  P1559
        return deep_get(self.json, "birthFullNameInNativeLanguageLabel.value")

    def get_birth_full_name(self) -> Union[str, None]:
        """
        P1477
        Example: `Doris Lessing` was born `Doris May Tayler`
        Or in the case of `Octavio Paz Lozano` where `Lozano` is dropped
        """
        return deep_get(self.json, "birthFullName.value")

    def get_date_of_birth(self) -> Union[str, None]:
        #  P569
        dob = deep_get(self.json, "dateOfBirthLabel.value")
        if dob:
            return dob.replace("T00:00:00Z", "")
        return None

    def get_place_of_birth(self) -> Union[str, None]:
        #  P19
        return deep_get(self.json, "placeOfBirthLabel.value")

    def get_date_of_death(self) -> Union[str, None]:
        #  P570
        dod = deep_get(self.json, "dateOfDeathLabel.value")
        if dod:
            return dod.replace("T00:00:00Z", "")
        return None

    def get_place_of_death(self) -> Union[str, None]:
        #  P20
        return deep_get(self.json, "placeOfDeathLabel.value")

    def get_manner_of_death(self) -> Union[str, None]:
        #  P1196
        return deep_get(self.json, "mannerOfDeathLabel.value")

    def get_cause_of_death(self) -> Union[str, None]:
        #  P509
        return deep_get(self.json, "causeOfDeathLabel.value")

    @staticmethod
    def _calculate_age_at_death(
        date_of_death: str, date_of_birth: str
    ) -> Union[int, None]:

        if date_of_death:
            date_of_death_datetime_object = parser.parse(date_of_death).date()
            date_of_birth_datetime_object = parser.parse(date_of_birth).date()
            return relativedelta(
                date_of_death_datetime_object, date_of_birth_datetime_object
            ).years
        return None

    def get_age_at_death(self) -> Union[int, None]:
        return deep_get(self.json, "ageAtDeathLabel.value")

    def get_place_of_burial(self) -> Union[str, None]:
        #  P119
        return deep_get(self.json, "placeOfBurialLabel.value")

    def get_native_language(self) -> Union[str, None]:
        #  P103
        return deep_get(self.json, "writingLanguageLabel.value")

    def get_writing_language(self) -> Union[str, None]:
        #  P6886
        return deep_get(self.json, "writingLanguageLabel.value")

    def get_occupation(self) -> Union[str, None]:
        #  P106
        return deep_get(self.json, "occupationLabel.value")

    def get_literary_movement(self) -> Union[str, None]:
        #  P135
        return deep_get(self.json, "literaryMovementLabel.value")

    def get_educated_at(self) -> Union[str, None]:
        #  P69
        return deep_get(self.json, "educatedAt.value")

    def get_lifestyle(self) -> Union[str, None]:
        #  P1576
        return deep_get(self.json, "lifestyleLabel.value")

    def get_religion(self) -> Union[str, None]:
        #  P140
        return deep_get(self.json, "religionLabel.value")

    def get_last_words(self) -> Union[str, None]:
        #  P1455
        return deep_get(self.json, "lastWordsLabel.value")

    def get_notable_works(self) -> Union[str, None]:
        #  P800
        return deep_get(self.json, "notableWorksLabel.value")

    def get_genre(self) -> Union[str, None]:
        #  P136
        return deep_get(self.json, "genreLabel.value")
