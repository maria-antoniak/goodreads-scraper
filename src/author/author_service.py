from typing import Dict, Union

from src.common.errors.errors import return_none_for_attribute_error

class AuthorService:
    def __init__(self, full_name: str, soup):

        self.full_name = full_name
        self.soup = soup

    def get_name_at_birth(self) -> Union[str, None]:
        """
        Example: `Doris Lessing` was born `Doris May Tayler`
        Or in the case of `Octavio Paz Lozano` where `Lozano` is dropped
        """
        pass

    @return_none_for_attribute_error
    def get_date_of_birth(self) -> Union[str, None]:
        return self.soup.find("span", {"class": "bday"}).text.strip()

    @return_none_for_attribute_error
    def get_city_of_birth(self) -> Union[str, None]:
        return self.soup.find("div", {"class": "birthplace"}).text.strip().split(",")[0]

    @staticmethod
    def get_country_of_birth(city_of_birth: str) -> Union[str, None]:
        import json

        f = open('/home/studs/PycharmProjects/goodreads-scraper/src/author/world.json')

        # returns JSON object as
        # a dictionary
        data = json.load(f)

        for country in data:
            if country['Capital'] == city_of_birth:
                return country['Country Name']
            pass

        f.close()
        return None

    @staticmethod
    def get_date_of_death() -> Union[str, None]:
        pass

    @staticmethod
    def get_country_of_death() -> Union[str, None]:
        pass

    @staticmethod
    def get_city_of_death() -> Union[str, None]:
        # i.e Resting Place
        pass

    @staticmethod
    def get_age_at_death() -> Union[int, None]:
        pass

    @staticmethod
    def get_resting_place() -> Union[str, None]:
        pass

    @staticmethod
    def get_nationality() -> Union[str, None]:
        pass

    @staticmethod
    def get_alma_mata() -> Union[str, None]:
        # Also referred to as `Education`
        pass

    @staticmethod
    def get_period() -> Union[str, None]:
        """
        This maybe tricky!
        """
        pass

    @staticmethod
    def get_literary_movement() -> Union[str, None]:
        """
        Also referred to on Wiki as `Style`
        """
        pass

    @staticmethod
    def get_notable_works() -> Union[Dict, None]:
        """
        Title, URL, Publication Date
        """
        pass

    @staticmethod
    def get_notable_awards() -> Union[Dict, None]:
        """
        Name, Link, Year Received
        """
        pass

    @staticmethod
    def get_language() -> Union[str, None]:
        pass

    @staticmethod
    def get_occupation() -> Union[str, None]:
        pass

    @staticmethod
    def get_pen_name() -> Union[str, None]:
        pass

    @staticmethod
    def get_gender() -> Union[str, None]:
        pass

    @staticmethod
    def get_genre() -> Union[str, None]:
        pass

    @staticmethod
    def get_years_active() -> Union[Dict, None]:
        return {"activeFrom": 1000, "activeTo": 2000}
