import pytest

from main import set_testing


@pytest.fixture
def app():
    return set_testing()


@pytest.fixture
async def cli(aiohttp_client, app):
    client = await aiohttp_client(app)
    yield client
