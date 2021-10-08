from dataclasses import dataclass
from typing import Union, List

from dataclasses_json.api import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AuthorModel:
    age_at_death: Union[int, None]
    birth_full_name: Union[str, None]
    birth_full_name_in_native_language: Union[str, None]
    cause_of_death: Union[str, None]
    country_of_citizenship: Union[str, None]
    date_of_birth: Union[str, None]
    date_of_death: Union[str, None]
    educated_at: Union[str, None]
    gender: Union[str, None]
    genre: Union[str, None]
    lifestyle: Union[str, None]
    literary_movement: Union[str, None]
    manner_of_death: Union[str, None]
    native_language: Union[str, None]
    notable_works: Union[str, None]
    occupation: Union[str, None]
    place_of_birth: Union[str, None]
    place_of_burial: Union[str, None]
    place_of_death: Union[str, None]
    religion: Union[str, None]
    writing_language: Union[str, None]
