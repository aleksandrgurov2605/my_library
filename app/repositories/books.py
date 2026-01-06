from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.books import BooksModel
from app.schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, book: SBookAdd, session: AsyncSession):
        book = BooksModel(**book.model_dump())

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def find_all(cls, session: AsyncSession):
        stmt = select(BooksModel)

        result = await session.execute(stmt)

        all_books = result.scalars().all()
        return all_books

    @classmethod
    async def fetch_one(cls, session: AsyncSession, **filter_by):
        stmt = select(BooksModel).filter_by(**filter_by)

        result = (await session.execute(stmt)).scalar_one_or_none()

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found/Книга не найдена")

        return result

