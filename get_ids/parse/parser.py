from typing import Union

import bs4
from requests.models import Response


from get_ids.errors.errors import return_none_for_attribute_error


@return_none_for_attribute_error
def parse_response(response: Union[Response, None]) -> Union[bs4.BeautifulSoup, None]:
    return bs4.BeautifulSoup(response.text, "html.parser")
