from src.common.utils.dict_operators import sort_by_value


class TestDictOperators:
    def setup_method(self):
        self.unordered_distribution_dict = {
            "fiveStar": 1127400,
            "fourStar": 731528,
            "oneStar": 32211,
            "threeStar": 360699,
            "twoStar": 78959,
        }

    def test_sort_by_value(self):
        expected = [
            ("fiveStar", 1127400),
            ("fourStar", 731528),
            ("threeStar", 360699),
            ("twoStar", 78959),
            ("oneStar", 32211),
        ]
        assert sort_by_value(self.unordered_distribution_dict) == expected
