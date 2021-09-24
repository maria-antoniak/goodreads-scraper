import pytest
import requests
import responses
from requests.models import Response

from typing import Generator

from src.common.network.network import get

from aiohttp.client_exceptions import ClientConnectionError

# TODO: We need to figure out how to mock aiohttp

# class TestNetwork:
#     def setup_method(self):
#         self.url = "https://www.goodreads.com/search?q=Kitchen%20-%20Banana%20Yoshimoto"
#
#     @responses.activate
#     def test_get_should_return_a_list_of_bytes_where_response_is_equal_to_200(
#         self,
#     ):
#         responses.add(responses.GET, self.url, status=200)
#         resp = get([self.url])
#         assert [type(r) for r in resp] == [bytes]

    # @responses.activate
    # def test_get_should_return_none_where_a_connection_error_is_thrown(self):
    #     responses.add(responses.GET, self.url, body=ClientConnectionError)
    #     assert get([""]) is None
    #
    # @responses.activate
    # @pytest.mark.parametrize(
    #     "status_code, expected",
    #     [(404, None), (403, None), (500, None), (503, None), (504, None)],
    # )
    # def test_get_should_return_none_where_response_is_not_equal_to_200(
    #     self, status_code, expected
    # ):
    #     responses.add(responses.GET, self.url, status=status_code)
    #     resp = get(self.url)
    #     assert resp == expected