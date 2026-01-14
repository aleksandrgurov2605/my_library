from fastapi import HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.books import BooksModel
from app.schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, book: SBookAdd, session: AsyncSession):
        """
        Добавляет одну книгу в БД.
        :param book:
        :param session:
        :return:
        """
        book = BooksModel(**book.model_dump())

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def find_all(cls, session: AsyncSession):
        """
        Возвращает все книги из БД.
        :param session:
        :return:
        """
        stmt = select(BooksModel)

        result = await session.execute(stmt)

        all_books = result.scalars().all()
        return all_books

    @classmethod
    async def fetch_one(cls, book_id, session: AsyncSession):
        """
        Возвращает одну книгу из БП по параметру book_id.
        :param book_id:
        :param session:
        :return:
        """
        stmt = select(BooksModel).where(BooksModel.id == book_id)

        result = (await session.execute(stmt)).scalar_one_or_none()

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found/Книга не найдена",
            )

        return result

    @classmethod
    async def find_by_status(cls, is_read, session: AsyncSession):
        """
        Возвращает книги из БД с определенным статусом прочтения,
        согласно параметру is_read. /
        Производит фильтрацию по параметру is_read.
        :param is_read:
        :param session:
        :return:
        """
        stmt = select(BooksModel).where(BooksModel.is_read == is_read)

        result = await session.execute(stmt)

        all_books = result.scalars().all()

        if len(all_books) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No books with this status were found./"
                       "Книг с данным статусом не найдено",
            )

        return all_books

    @classmethod
    async def edit_one(cls, book: SBookAdd, book_id, session: AsyncSession):
        """
        Редактирует книгу по book_id, данные из БД
        заменяются на данные из book: SBookAdd.
        :param book:
        :param book_id:
        :param session:
        :return:
        """
        stmt = select(BooksModel).where(BooksModel.id == book_id)

        edited_book = (await session.execute(stmt)).scalar_one_or_none()

        if edited_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found/Книга не найдена",
            )

        await session.execute(
            update(BooksModel)
            .where(BooksModel.id == edited_book.id)
            .values(**book.model_dump())
        )

        await session.commit()
        await session.refresh(edited_book)

        return edited_book

    @classmethod
    async def delete_one(cls, book_id: int, session: AsyncSession):
        """
        Удаляет из базы данных книгу по book_id.
        :param book_id:
        :param session:
        :return:
        """
        stmt = select(BooksModel).where(BooksModel.id == book_id)

        deleted_book = (await session.execute(stmt)).scalar_one_or_none()

        if deleted_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found/Книга не найдена",
            )

        stmt = delete(BooksModel).where(BooksModel.id == deleted_book.id)

        await session.execute(stmt)
        await session.commit()

        return deleted_book
