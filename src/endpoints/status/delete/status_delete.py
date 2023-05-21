import logging

from fastapi import Depends, HTTPException, Path
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from starlette import status

from src.dependencies import get_current_librarian, get_db
from src.endpoints.status.router_init import router
from src.models import all_models


@router.delete(
    "/{status_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def status_delete(
    status_id: int = Path(gt=-1),
    db: Session = Depends(get_db),
    librarian=Depends(get_current_librarian),
) -> None:
    """ "
    Deletes the Status on status ID.
    Params
    ------
    JWT token of librarian.\n
    status_id: int
    Returns
    ------
    Status code 204 NO_CONTENT
    """
    logging.info(f"Deleting status {status_id} -- {__name__}")
    found_status = db.scalar(
        select(all_models.Status).where(all_models.Status.id == status_id)
    )
    if not found_status:
        logging.warning("Status not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Status not found"
        )
    try:
        db.delete(found_status)
        db.commit()
        logging.info("Deleted status")
    except Exception as e:
        logging.exception("Error deleting status. Details = " + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
