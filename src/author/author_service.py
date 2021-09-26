import bs4

from src.common.utils.string_operators import split_on_delimiter


class AuthorService:
    def __init__(self, author_full_name: str):

        self.author_full_name = author_full_name

    @staticmethod
    def get_author_date_of_birth() -> str:
        pass

    @staticmethod
    def get_author_place_of_birth() -> str:
        pass

    @staticmethod
    def get_author_date_of_death() -> str:
        pass

    @staticmethod
    def get_author_place_of_death() -> str:
        pass

    @staticmethod
    def get_author_country() -> str:
        pass

    @staticmethod
    def get_author_gender() -> str:
        pass

    @staticmethod
    def get_author_race() -> str:
        pass

    @staticmethod
    def get_author_period() -> str:
        """
        This maybe tricky!
        """
        pass

    @staticmethod
    def get_author_genres() -> [str]:
        pass

    @staticmethod
    def get_author_notable_works() -> [str]:
        pass

    @staticmethod
    def get_author_years_active() -> {}:
        return {
            'activeFrom': 1000,
            'activeTo': 2000

        }
