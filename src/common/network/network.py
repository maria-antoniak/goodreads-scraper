import asyncio
from typing import Union

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError


def get(urls: [str]) -> [bytes]:
    return asyncio.run(_get_response(urls))


async def _get_response(urls: [str]) -> [bytes]:
    tasks = []
    for url in urls:
        tasks.append(asyncio.ensure_future(_get_request(url)))

    return await asyncio.gather(*tasks)


async def _get_request(url) -> Union[bytes, None]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.read()
    except ClientConnectionError:
        return None
