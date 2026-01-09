from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BooksModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int|None]
    pages: Mapped[int|None]
    is_read: Mapped[bool] = mapped_column(default=False)
