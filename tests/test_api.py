import pytest


@pytest.mark.asyncio
async def test_add_book(client):
    r = await client.post("/books", json={
        'title': 'Test Book',
        'author': 'Me',
        'year': 2026,
        'pages': 11,
        'is_read': 'false'
    })
    assert r.status_code == 201
    created = r.json()
    assert created["title"] == "Test Book"
    assert created["author"] == "Me"
    assert "id" in created


@pytest.mark.asyncio
async def test_get_all_books(client):
    book_1 = await client.post("/books", json={
        'title': 'Test Book 1',
        'author': 'Me?',
        'year': 1999,
        'pages': 11,
        'is_read': 'true'
    })
    book_2 = await client.post("/books", json={
        'title': 'Test Book 2',
        'author': 'You?',
        'year': 2025,
        'pages': 100,
        'is_read': 'false'
    })
    assert book_1.status_code == 201
    assert book_2.status_code == 201

    books_from_db = await client.get("/books")
    assert books_from_db.status_code == 200
    assert len(books_from_db.json()) == 2
    assert books_from_db.json()[0]["title"] == 'Test Book 1'
    assert books_from_db.json()[1]["title"] == 'Test Book 2'


@pytest.mark.asyncio
async def test_get_book_by_id(client):
    book = await client.post("/books", json={
        'title': 'Test Book',
        'author': 'Me',
        'year': 2026,
        'pages': 11,
        'is_read': 'false'
    })
    assert book.status_code == 201

    book_from_db = await client.get("/books/1")
    assert book_from_db.status_code == 200
    assert book_from_db.json()["title"] == "Test Book"


@pytest.mark.asyncio
async def test_get_book_by_id_not_found(client):
    book = await client.post("/books", json={
        'title': 'Test Book',
        'author': 'Me',
        'year': 2026,
        'pages': 11,
        'is_read': 'false'
    })
    assert book.status_code == 201

    book_from_db = await client.get("/books/99")
    assert book_from_db.status_code == 404
    assert book_from_db.json()["detail"] == "Book not found/Книга не найдена"


