import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from tests.fastapi.app import app
from tests.fastapi.models import (
    DoorAPI,
    House,
    HouseAPI,
    Person,
    RoofAPI,
    WindowAPI,
)


@pytest.fixture(autouse=True)
async def api_client(clean_db):
    """api client fixture."""
    async with LifespanManager(app, startup_timeout=100, shutdown_timeout=100):
        server_name = "http://localhost"
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=server_name
        ) as ac:
            yield ac


@pytest.fixture(autouse=True)
async def clean_db(db):
    models = [House, Person, HouseAPI, WindowAPI, DoorAPI, RoofAPI]
    yield None

    for model in models:
        await model.get_pymongo_collection().drop()
        await model.get_pymongo_collection().drop_indexes()
