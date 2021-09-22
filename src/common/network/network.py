import asyncio
from typing import Union

import aiohttp
import bs4


def get(urls: [str]) -> [bytes]:
    return asyncio.run(_get_response(urls))


async def _get_request(url) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()


async def _get_response(urls: [str]) -> [bytes]:
    tasks = []
    for url in urls:
        tasks.append(asyncio.ensure_future(_get_request(url)))

    return await asyncio.gather(*tasks)


def get_soup(response: Union[bytes, None]) -> Union[bs4.BeautifulSoup, None]:
    return bs4.BeautifulSoup(response, "html.parser")
