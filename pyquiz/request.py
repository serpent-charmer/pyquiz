from typing import List
import aiohttp


async def get_questions(count):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://jservice.io/api/random?count={count}') as resp:
            if resp.status == 200:
                quiz = await resp.json()
                return quiz