from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
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

    @classmethod
    async def edit_one(cls, book: SBookAdd, session: AsyncSession, **filter_by):
        stmt = select(BooksModel).filter_by(**filter_by)

        edited_book = (await session.execute(stmt)).scalar_one_or_none()

        if edited_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found/Книга не найдена")

        await session.execute(
            update(BooksModel).where(BooksModel.id == edited_book.id).values(**book.model_dump())
        )

        await session.commit()
        await session.refresh(edited_book)

        return edited_book

    @classmethod
    async def delete_one(cls, session: AsyncSession, **filter_by):
        stmt = select(BooksModel).filter_by(**filter_by)

        deleted_book = (await session.execute(stmt)).scalar_one_or_none()

        if deleted_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found/Книга не найдена")

        stmt = delete(BooksModel).where(BooksModel.id == deleted_book.id)

        await session.execute(stmt)

        await session.commit()


        return deleted_book

