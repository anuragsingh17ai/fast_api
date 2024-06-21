## here file name will always be same
## it is fixture and fixture are used to
## share data betweeen different test file

from typing import AsyncGenerator, Generator
from httpx import AsyncClient
import pytest
from fastapi.testclient import TestClient

from socialMedia.main import app
from socialMedia.routers.post import comment_table, post_table

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield

@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac

