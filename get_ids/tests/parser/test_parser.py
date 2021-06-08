from get_ids.parse.parser import parse_response


class TestParser:
    def test_ut_parse_response_should_return_none_where_response_is_equal_to_none(self):
        assert parse_response(None) is None
