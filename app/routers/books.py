from fastapi import APIRouter
from starlette import status

from app.db.db_depends import SessionDep
from app.repositories.books import BookRepository
from app.schemas.books import SBookRead, SBookAdd

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


@books_router.get("")
async def get_all_books(
        db: SessionDep
) -> list[SBookRead]:
    books = await BookRepository.find_all(db)
    return books


@books_router.get("/{id}")
async def get_book_by_id(
        book_id: int,
        db: SessionDep
) -> SBookRead:
    books = await BookRepository.fetch_one(db, id=book_id)
    return books
