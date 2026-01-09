from fastapi import APIRouter, status

from app.db.db_depends import SessionDep
from app.repositories.books import BookRepository
from app.schemas.books import SBookAdd, SBookRead

books_router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@books_router.post("", response_model=SBookRead, status_code=status.HTTP_201_CREATED)
async def add_book(
        book: SBookAdd,
        db: SessionDep,
):
    book = await BookRepository.add_one(book, db)

    return book


@books_router.get("", response_model=list[SBookRead])
async def get_all_books(
        db: SessionDep,
        is_read: bool | None = None
):
    if is_read is not None:
        books = await BookRepository.find_by_status(is_read, db)
    else:
        books = await BookRepository.find_all(db)
    return books


@books_router.get("/{book_id}", response_model=SBookRead)
async def get_book_by_id(
        book_id: int,
        db: SessionDep
):
    books = await BookRepository.fetch_one(book_id, db)
    return books


@books_router.put("/{book_id}", response_model=SBookRead)
async def edit_book(
        book: SBookAdd,
        book_id: int,
        db: SessionDep
):
    book = await BookRepository.edit_one(book, book_id, db)
    return book


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        db: SessionDep
):
    await BookRepository.delete_one(book_id, db)
    return None
