import logging

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.copy.router_init import router
from src.exceptions import custom_exception
from src.models.copy import Copy


@router.delete("/{copy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def copy_delete(
    copy_id: int,
    db: Session = Depends(get_db),
    librarian: dict = Depends(get_current_librarian),  # noqa
) -> None:
    """
    Endpoint to delete a copy by ID.
    """
    logging.info(
        f"Book Delete with id :{copy_id} Request by Librarian {librarian['id']}"
    )

    copy_model = db.execute(select(Copy).where(Copy.id == copy_id)).scalars().first()

    if copy_model is None:
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Copy not found"
        )

    db.execute(delete(Copy).where(Copy.id == copy_id))
    db.commit()
    logging.info(
        f"Book Updated with id :{copy_id} Request by Librarian {librarian['id']}"
    )
