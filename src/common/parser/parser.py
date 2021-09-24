from typing import Union

import bs4

from src.common.errors.errors import return_none_for_type_error


@return_none_for_type_error
def parse(response: Union[bytes, None]) -> Union[bs4.BeautifulSoup, None]:
    return bs4.BeautifulSoup(response, "html.parser")
