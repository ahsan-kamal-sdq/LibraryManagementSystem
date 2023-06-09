import logging
from typing import Annotated, List

from fastapi import Depends, Query
from sqlalchemy import asc, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.author.router_init import router
from src.models.author import Author
from src.responses import custom_response


@router.get("", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_authors(
    db: Session = Depends(get_db),
    page_number: Annotated[int, Query(gt=0)] = 1,  # Default value is 1
    page_size: Annotated[int, Query(gt=0)] = 10,  # Default value is 10
) -> dict:
    """
    Returns all the Authors in DB.\n
    Params
    ------
    JWT token of user.\n
    Returns
    ------
     dict : A dict with status code, details and data
    """
    starting_index = (page_number - 1) * page_size
    logging.info(f"Getting all the authors -- {__name__}")
    authors = (
        db.execute(
            select(Author)
            .where(not_(Author.is_deleted))
            .order_by(asc(Author.id))
            .offset(starting_index)
            .limit(page_size)
        )
        .scalars()
        .all()
    )
    return custom_response(
        status_code=status.HTTP_200_OK,
        details="Authors fetched successfully!",
        data=authors,
    )
