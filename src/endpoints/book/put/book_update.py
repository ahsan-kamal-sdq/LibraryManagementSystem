import logging
from datetime import datetime

from fastapi import Depends
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.book.router_init import router
from src.exceptions import custom_exception
from src.models.author import Author
from src.models.book import Book
from src.models.genre import Genre
from src.models.language import Language
from src.responses import custom_response
from src.schemas.book import BookSchema


@router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=None)
async def book_update(
    book_id: int,
    book: BookSchema,
    librarian: dict = Depends(get_current_librarian),
    db: Session = Depends(get_db),
) -> dict:
    """
    Update an existing book by ID.
    """

    book_model = (
        db.execute(select(Book).where(and_(Book.id == book_id, not_(Book.is_deleted))))
        .scalars()
        .first()
    )

    if book_model is None:
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Book not found"
        )
    logging.info(
        f"Book with ID: {book_model.id} Update requested by Librarian {librarian['id']}"
    )

    language = (
        db.execute(select(Language).where(Language.id == book.language_id))
        .scalars()
        .first()
    )
    authors = (
        db.execute(select(Author).where(Author.id.in_(book.author_ids))).scalars().all()
    )
    genres = (
        db.execute(select(Genre).where(Genre.id.in_(book.genre_ids))).scalars().all()
    )

    book_model.title = book.title
    book_model.date_of_publication = datetime.strptime(
        book.date_of_publication, "%Y-%m-%d"
    ).date()
    book_model.description = book.description
    book_model.isbn = book.isbn
    book_model.language_id = book.language_id
    book_model.authors = authors
    book_model.genres = genres
    book_model.language = language

    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    book.id = book_model.id
    logging.info(
        f"Book with ID: {book_model.id} Updated by Librarian {librarian['id']}"
    )
    return custom_response(
        status_code=status.HTTP_200_OK, details="Book Updated", data=book.dict()
    )
