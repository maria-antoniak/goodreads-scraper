from src.common.parser.parser import parse


class TestParser:
    def test_parse_should_return_none_where_response_is_equal_to_none(self):
        assert parse(None) is None
