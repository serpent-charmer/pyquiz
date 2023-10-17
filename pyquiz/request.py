import sys
from traceback import print_exc, print_exception
from typing import List
import aiohttp


async def _get_questions(count):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://jservice.io/api/random?count={count}') as resp:
            if resp.status == 200:
                quiz = await resp.json()
                return quiz
            
async def get_questions(count):
    try:
        return await _get_questions(count)
    except aiohttp.ClientConnectionError as e:
        print_exc(file=sys.stderr)