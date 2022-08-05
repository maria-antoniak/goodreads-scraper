from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json.api import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AuthorModel:
    age_at_death: Optional[str]
    birth_full_name: Optional[str]
    birth_full_name_in_native_language: Optional[str]
    cause_of_death: Optional[str]
    country_of_citizenship: Optional[str]
    date_of_birth: Optional[str]
    date_of_death: Optional[str]
    educated_at: Optional[List[str]]
    gender: Optional[str]
    genres: Optional[List[str]]
    last_words: Optional[str]
    lifestyle: Optional[List[str]]
    literary_movements: Optional[List[str]]
    manner_of_death: Optional[str]
    native_language: Optional[str]
    notable_works: Optional[List[str]]
    occupations: Optional[List[str]]
    place_of_birth: Optional[str]
    place_of_burial: Optional[str]
    place_of_death: Optional[str]
    religion: Optional[str]
    work_period_start_year: Optional[int]
    writing_languages: Optional[List[str]]
