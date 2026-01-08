import pytest
import pytest_mock
from fastapi import HTTPException
from starlette import status

from app.repositories.books import BookRepository
from app.models.books import BooksModel
from app.schemas.books import SBookAdd


@pytest.mark.asyncio
async def test_add_one(mocker: pytest_mock.MockerFixture):
    mock_session = mocker.AsyncMock()

    book_data = SBookAdd(title="Название", author="Автор", year=2021, pages=11, is_read=True)
    mock_session.execute.return_value = book_data
    mock_session.add = mocker.Mock()
    mock_session.commit = mocker.AsyncMock()
    mock_session.refresh = mocker.AsyncMock()

    result = await BookRepository.add_one(book_data, mock_session)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

    assert hasattr(result, "title")
    assert result.title == "Название"
    assert result.year == 2021


@pytest.mark.asyncio
async def test_find_all(mocker: pytest_mock.MockerFixture):
    mock_session = mocker.AsyncMock()

    mock_books = mocker.Mock()
    mock_books.scalars.return_value.all.return_value = [
        BooksModel(id=1, title="Mock book_1", author="Mock Author_1", year=1999, pages=100),
        BooksModel(id=1, title="Mock book_2", author="Mock Author_2", year=2026, pages=11, is_read=True),
    ]
    mock_session.execute.return_value = mock_books
    books = await BookRepository.find_all(mock_session)

    mock_session.execute.assert_awaited()
    assert len(books) == 2
    assert books[0].title == "Mock book_1"
    assert books[0].pages == 100
    assert books[1].year == 2026


@pytest.mark.asyncio
async def test_fetch_one_found(mocker: pytest_mock.MockerFixture):
    mock_session = mocker.AsyncMock()

    mock_book = mocker.Mock()
    mock_book.scalar_one_or_none.return_value = BooksModel(
        id=1,
        title="Mock book",
        author="Mock Author",
        year=2020,
        pages=11,
        is_read=True
    )
    mock_session.execute.return_value = mock_book
    result = await BookRepository.fetch_one(1, mock_session)

    assert isinstance(result, BooksModel)
    assert result.id == 1
    assert result.title == "Mock book"


@pytest.mark.asyncio
async def test_fetch_one_not_found(mocker: pytest_mock.MockerFixture):
    mock_session = mocker.AsyncMock()

    mock_book = mocker.Mock()
    mock_book.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_book

    with pytest.raises(HTTPException) as exc_info:
        await BookRepository.fetch_one(999, mock_session)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "Book not found" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_edit_one_found(mocker: pytest_mock.MockerFixture):
    mock_session = mocker.AsyncMock()

    existing_book = BooksModel(id=1, title="Old Title", author="Old Author", year=2010, pages=150)
    mock_result = mocker.Mock()
    mock_result.scalar_one_or_none.return_value = existing_book
    mock_session.execute.return_value = mock_result

    mock_session.execute_update = mocker.AsyncMock()

    new_data = SBookAdd(title="New Title", author="New Author", year=2015, pages=200, is_read=True)
    result = await BookRepository.edit_one(new_data, 1, mock_session)

    mock_session.execute.assert_awaited()
    mock_session.commit.assert_awaited()
    mock_session.refresh.assert_awaited_with(existing_book)
    assert result.title == "Old Title"


@pytest.mark.asyncio
async def test_edit_one_not_found(mocker: pytest_mock.MockerFixture):
    mock_session = mocker.AsyncMock()

    mock_book = mocker.Mock()
    mock_book.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_book

    with pytest.raises(HTTPException) as exc_info:
        await BookRepository.edit_one(
            SBookAdd(title="Test", author="Test", year=2000, pages=300, is_read=False),
            999,
            mock_session
        )
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "Book not found" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_delete_one_found(mocker):
    mock_session = mocker.AsyncMock()
    mock_result = mocker.Mock()
    mock_result.scalar_one_or_none.return_value = BooksModel(id=1, title="Book to delete", author="A", year=2000, pages=100)
    mock_session.execute = mocker.AsyncMock(return_value=mock_result)

    result = await BookRepository.delete_one(1, mock_session)

    mock_session.execute.assert_awaited()
    mock_session.commit.assert_awaited()
    assert isinstance(result, BooksModel)
    assert result.id == 1

@pytest.mark.asyncio
async def test_delete_one_not_found(mocker):
    mock_session = mocker.AsyncMock()
    mock_result = mocker.Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = mocker.AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException)  as exc_info:
        await BookRepository.delete_one(999, mock_session)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "Book not found" in str(exc_info.value.detail)