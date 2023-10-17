import asyncio
import selectors
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from sqlalchemy import NullPool, select
from pyquiz import app
from httpx import AsyncClient
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from pyquiz.db import DATABASE_URL, SessionDependency, get_session
from pyquiz.model import Question, QuizBase


test_schema = "test"
engine = create_async_engine(DATABASE_URL, echo=False, execution_options={
                             "schema_translate_map": {None: test_schema}},
                             poolclass=NullPool)


@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session")
async def client(myapp: FastAPI):
    async with AsyncClient(app=myapp, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
def event_loop():
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    yield loop
    loop.close()


async def sess() -> AsyncIterator[AsyncSession]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_schema():
    async with engine.begin() as conn:
        check = await conn.run_sync(engine.dialect.has_schema, test_schema)
        if not check:
            await conn.execute(CreateSchema(test_schema))


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_init():
    async with engine.begin() as conn:
        await conn.run_sync(QuizBase.metadata.drop_all)
        await conn.run_sync(QuizBase.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
def myapp():
    app.dependency_overrides[get_session] = sess
    return app


@pytest.mark.anyio
async def test_add_quiz(client: AsyncClient):
    rs = await client.post("/quiz/random", json={"question_num": 1})
    rs = await client.get("/question/get", params={"question_id": 1})
    assert rs.content != b'null'

@pytest.mark.anyio
async def test_no_question(client: AsyncClient):
    rs = await client.get("/question/get", params={"question_id": 1})
    assert rs.content == b'null'