from dataclasses import dataclass
from typing import Union

from dataclasses_json.api import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AuthorModel:
    name_at_birth: Union[str, None]
