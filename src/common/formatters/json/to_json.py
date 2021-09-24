# same imports as above, with the additional `LetterCase` import
from dataclasses import dataclass
from dataclasses_json.api import dataclass_json, LetterCase

from typing import Dict

def to_json(model) -> Dict:
    return model.to_dict()
