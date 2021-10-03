import asyncio
from typing import Union

import aiohttp
import wikipedia
from aiohttp.client_exceptions import ClientConnectionError
from wikipedia.wikipedia import WikipediaPage


def get(urls: [str]) -> [bytes]:
    return asyncio.run(_get_response(urls))


async def _get_request(url) -> Union[bytes, None]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.read()
    except ClientConnectionError:
        return None


async def _get_response(urls: [str]) -> [bytes]:
    tasks = []
    for url in urls:
        tasks.append(asyncio.ensure_future(_get_request(url)))

    return await asyncio.gather(*tasks)


def search_for_wikipedia_result(author_full_name: str) -> Union[WikipediaPage, None]:
    results = wikipedia.page(author_full_name)
    if results:
        return results


def _is_wikipedia_result_an_exact_match(
    author_full_name: str, wikipedia_result: WikipediaPage
) -> bool:
    return True if author_full_name in wikipedia_result.title else False
