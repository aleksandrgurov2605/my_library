from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import Base, async_engine
from app.routers.books import books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(books_router)
