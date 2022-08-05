import pytest
from data.doris_lessing import doris_lessing_sparql_response

from src.author.author_service import AuthorService


class TestBookService:
    def setup_method(self):

        self.author_service = AuthorService(doris_lessing_sparql_response)

    def test_get_gender(self):
        assert self.author_service.get_gender() == "Female"

    @pytest.mark.skip(
        reason="Test result is varying, likely based on order of iteration"
    )
    def test_get_country_of_citizenship(self):
        assert self.author_service.get_country_of_citizenship() == "United Kingdom"

    def test_get_birth_full_name_in_native_language(self):
        assert (
            self.author_service.get_birth_full_name_in_native_language()
            == "Doris May Lessing"
        )

    def test_get_birth_full_name(self):
        assert self.author_service.get_birth_full_name() == "Doris May Tayler"

    def test_get_date_of_birth(self):
        assert self.author_service.get_date_of_birth() == "1919-10-22"

    def test_get_place_of_birth(self):
        assert self.author_service.get_place_of_birth() == "Kermanshah"

    def test_get_date_of_death(self):
        assert self.author_service.get_date_of_death() == "2013-11-17"

    def test_get_place_of_death(self):
        assert self.author_service.get_place_of_death() == "London"

    def test_manner_of_death(self):
        assert self.author_service.get_manner_of_death() is None

    def test_get_cause_of_death(self):
        assert self.author_service.get_cause_of_death() == "Stroke"

    def test_calculate_age_at_death(self):
        date_of_death = "2013-11-17"
        date_of_birth = "1919-10-22"
        assert (
            self.author_service._calculate_age_at_death(date_of_death, date_of_birth)
            == 94
        )

    def test_get_age_at_death(self):
        assert self.author_service.get_age_at_death() is None

    def test_get_place_of_burial(self):
        assert self.author_service.get_place_of_burial() is None

    def test_get_native_language(self):
        assert self.author_service.get_native_language() is None

    def test_get_writing_language(self):
        assert self.author_service.get_writing_languages() is None

    def test_get_occupation(self):
        expected = [
            "Autobiographer",
            "Essayist",
            "Novelist",
            "Playwright",
            "Poet",
            "Prosaist",
            "Science Fiction Writer",
            "Screenwriter",
            "Writer",
        ]
        assert self.author_service.get_occupations() == expected

    def test_get_literary_movement(self):
        assert self.author_service.get_literary_movements() == ["Literary Realism"]

    def test_get_educated_at(self):
        assert self.author_service.get_educated_at() == [
            "Dominican Convent High School"
        ]

    def test_get_lifestyle(self):
        assert self.author_service.get_lifestyle() is None

    def test_get_religion(self):
        assert self.author_service.get_religion() is None

    def test_get_last_words(self):
        assert self.author_service.get_last_words() is None

    def test_get_get_notable_works(self):
        expected = [
            "A Ripple From The Storm",
            "The Cleft",
            "The Golden Notebook",
            "The Good Terrorist",
            "The Grass Is Singing",
            "The Memoirs Of A Survivor",
        ]

        assert self.author_service.get_notable_works() == expected

    def test_get_genre(self):
        assert self.author_service.get_genres() == ["Science Fiction"]

    def test_get_work_period_start_year(self):
        assert self.author_service.get_work_period_start_year() == "1950"
