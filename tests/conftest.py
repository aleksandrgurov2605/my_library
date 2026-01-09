import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.database import Base
from app.db.db_depends import get_async_db
from app.main import app as prod_app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # отдельная БД для тестов


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(test_engine):
    return async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
async def app_test(async_session):
    async def _get_db():
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.rollback()

    prod_app.dependency_overrides[get_async_db] = _get_db
    yield prod_app
    prod_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app_test: FastAPI):
    transport = ASGITransport(app=app_test)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c


