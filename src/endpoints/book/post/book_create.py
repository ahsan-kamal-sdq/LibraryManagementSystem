import logging
from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.book.router_init import router
from src.exceptions import custom_exception
from src.models.author import Author
from src.models.book import Book
from src.models.copy import Copy
from src.models.genre import Genre
from src.models.language import Language
from src.responses import custom_response
from src.schemas.book import BookSchema


@router.post("/", status_code=status.HTTP_201_CREATED)
async def book_create(
    book: BookSchema,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa,
) -> dict:
    """
    Endpoint to create a book
    """
    logging.info(f"Book Create Request by Librarian {librarian['id']}")

    language = (
        db.execute(select(Language).where(Language.id == book.language_id))
        .scalars()
        .first()
    )
    if language is None:
        logging.error("No language found while creating book")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Language not found"
        )
    authors = (
        db.execute(select(Author).where(Author.id.in_(book.author_ids))).scalars().all()
    )
    if len(authors) == 0:
        logging.error("No author found while creating book")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Author not found"
        )
    genres = (
        db.execute(select(Genre).where(Genre.id.in_(book.genre_ids))).scalars().all()
    )
    if len(genres) == 0:
        logging.error("No genre found while creating book")
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Genre not found"
        )
    book_model = Book()
    book_model.title = book.title
    book_model.date_of_publication = datetime.strptime(
        book.date_of_publication, "%Y-%m-%d"
    ).date()
    book_model.description = book.description
    book_model.isbn = book.isbn
    book_model.language_id = book.language_id
    book_model.authors.extend(authors)
    book_model.genres.extend(genres)
    book_model.language = language

    try:
        db.add(book_model)
        db.commit()
        logging.info(
            f"Book with ID: {book_model.id} Created by Librarian {librarian['id']}"
        )
        book_id = book_model.id
        copy_models = []
        print(book.no_of_copies)
        for i in range(book.no_of_copies):
            copy = Copy(book_id=book_id, language_id=book.language_id, status_id=1)
            copy_models.append(copy)

        db.add_all(copy_models)
        db.commit()
        logging.info(
            f"{book.no_of_copies} Copies created with Book ID: {book_model.id} Created by Librarian {librarian['id']}"
        )
    except IntegrityError as e:
        print(e)
        raise custom_exception(
            status_code=status.HTTP_409_CONFLICT, details="Book already exist"
        )

    book.id = book_model.id

    return custom_response(
        status_code=status.HTTP_201_CREATED,
        details="Book created successfully!",
        data=book,
    )
