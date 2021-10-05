from data.doris_lessing import doris_lessing_sparql_response

from src.author.author_service import AuthorService


class TestBookService:
    def setup_method(self):

        self.author_service = AuthorService(doris_lessing_sparql_response)

    def test_get_gender(self):
        assert self.author_service.get_gender() == "female"

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
        assert self.author_service.get_date_of_birth() == "1919-10-22T00:00:00Z"

    def test_get_place_of_birth(self):
        assert self.author_service.get_place_of_birth() is None

    def test_get_date_of_death(self):
        assert self.author_service.get_date_of_death() == "2013-11-17T00:00:00Z"

    def test_get_place_of_death(self):
        assert self.author_service.get_place_of_death() is None

    def test_manner_of_death(self):
        assert self.author_service.get_manner_of_death() is None

    def test_get_cause_of_death(self):
        assert self.author_service.get_cause_of_death() is None

    def test_calculate_age_at_death(self):
        date_of_death = "2013-11-17T00:00:00Z"
        date_of_birth = "1919-10-22T00:00:00Z"
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
        assert self.author_service.get_writing_language() is None

    def test_get_occupation(self):
        assert self.author_service.get_occupation() == "essayist"

    def test_get_literary_movement(self):
        assert self.author_service.get_literary_movement() == "literary realism"

    def test_get_educated_at(self):
        assert self.author_service.get_educated_at() is None

    def test_get_lifestyle(self):
        assert self.author_service.get_lifestyle() is None

    def test_get_religion(self):
        assert self.author_service.get_religion() is None

    def test_get_last_words(self):
        assert self.author_service.get_last_words() is None

    def test_get_get_notable_works(self):
        assert self.author_service.get_notable_works() == "A Ripple from the Storm"

    def test_get_genre(self):
        assert self.author_service.get_genre() == "science fiction"
