import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from project.components.health.db_checker import DBChecker
from project.components.health.dependencies import get_db_checker

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/health', tags=['Health'])


@router.get('/', summary='Healthcheck if database is online.')
async def get_db_status(db_checker: DBChecker = Depends(get_db_checker)) -> Response:
    """Return response that represents status of the database."""

    logger.info('Checking if database is online.')

    is_online = await db_checker.is_online()

    logger.info('Received is_online status.', extra={'is_online': is_online})

    response = Response(status_code=204)
    if not is_online:
        response = JSONResponse(status_code=503)

    return response
