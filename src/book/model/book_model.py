from dataclasses import dataclass
from typing import Union, Dict
from dataclasses_json.api import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)  # now all fields are encoded/decoded from camelCase@dataclass
@dataclass
class BookModel:
    title_id: Union[str, None]
    numeric_id: Union[int, None]
    title: Union[str, None]
    series: Union[str, None]
    book_series_uri: Union[str, None]
    isbn: Union[str, None]
    isbn13: Union[str, None]
    author_full_name: Union[str, None]
    author_first_name: Union[str, None]
    author_last_name: Union[str, None]
    number_of_pages: Union[int, None]
    genres: Union[str, None]
    primary_genre: Union[str, None]
    # shelves: Union[Dict, None]
    # lists: Union[Dict, None]
    # num_ratings: Union[int, None]
    # num_reviews: Union[int, None]
    # average_rating: Union[float, None]
    # rating_distribution: Union[Dict, None]
