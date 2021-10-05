from dataclasses import dataclass
from typing import Union

from dataclasses_json.api import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AuthorModel:
    gender: Union[str, None]
    country_of_citizenship: Union[str, None]
    birth_full_name_in_native_language: Union[str, None]
    birth_full_name: Union[str, None]
    date_of_birth: Union[str, None]
    place_of_birth: Union[str, None]
    date_of_death: Union[str, None]
    place_of_death: Union[str, None]
    manner_of_death: Union[str, None]
    cause_of_death: Union[str, None]
    age_at_death: Union[int, None]
    place_of_burial: Union[str, None]
    native_language: Union[str, None]
    writing_language: Union[str, None]
    occupation: Union[str, None]
    literary_movement: Union[str, None]
    educated_at: Union[str, None]
    lifestyle: Union[str, None]
    religion: Union[str, None]
    notable_works: Union[str, None]
    genre: Union[str, None]
