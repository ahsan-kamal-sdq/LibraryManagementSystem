import logging

from fastapi import Depends, Path
from sqlalchemy import and_, not_, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_db
from src.endpoints.status.router_init import router
from src.exceptions import custom_exception
from src.models import all_models
from src.responses import custom_response


@router.get("/{status_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_status_by_id(
    status_id: int = Path(gt=-1), db: Session = Depends(get_db)
) -> dict:
    """
    This function will be used to get a status by id.
    Parameters:
        status_id: The id of the status.
        db: The database session.
    Returns:
        dict: A dictionary with the status code and message and data.
    """
    logging.info("Fetching status by id" + str(status_id))
    found_status = db.scalars(
        select(all_models.Status).where(
            and_(all_models.Status.id == status_id, not_(all_models.Status.is_deleted))
        )
    ).first()
    if not found_status:
        raise custom_exception(
            status_code=status.HTTP_404_NOT_FOUND, details="Status not found"
        )
    logging.info("Status found")
    return custom_response(
        status_code=status.HTTP_200_OK, details="Status found", data=found_status
    )
