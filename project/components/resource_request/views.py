from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.resource_request.crud import ResourceRequestCRUD
from project.components.resource_request.schemas import ResourceRequestCreateSchema
from project.components.resource_request.schemas import ResourceRequestListResponseSchema
from project.components.resource_request.schemas import ResourceRequestResponseSchema
from project.components.resource_request.schemas import ResourceRequestUpdateSchema
from project.dependencies import get_db_session

router = APIRouter(prefix='/resource-requests', tags=['Resource Requests'])


@router.get('/', summary='List all resource requests.', response_model=ResourceRequestListResponseSchema)
async def list_resource_requests(
    db_session: AsyncSession = Depends(get_db_session),
) -> ResourceRequestListResponseSchema:
    """List all resource requests."""

    resource_request_crud = ResourceRequestCRUD(db_session)

    resource_requests = await resource_request_crud.list()

    response = ResourceRequestListResponseSchema(num_of_pages=0, page=0, total=0, result=resource_requests)

    return response


@router.get(
    '/{resource_request_id}',
    summary='Get a resource request by id.',
    response_model=ResourceRequestResponseSchema,
)
async def get_resource_request(
    resource_request_id: UUID, db_session: AsyncSession = Depends(get_db_session)
) -> ResourceRequestResponseSchema:
    """Get a resource request by id."""

    resource_request_crud = ResourceRequestCRUD(db_session)

    resource_request = await resource_request_crud.retrieve_by_id(resource_request_id)

    return resource_request


@router.post('/', summary='Create a new resource request.', response_model=ResourceRequestResponseSchema)
async def create_resource_request(
    body: ResourceRequestCreateSchema, db_session: AsyncSession = Depends(get_db_session)
) -> ResourceRequestResponseSchema:
    """Create a new resource request."""

    resource_request_crud = ResourceRequestCRUD(db_session)

    async with resource_request_crud:
        resource_request = await resource_request_crud.create(body)

    return resource_request


@router.patch(
    '/{resource_request_id}', summary='Update a resource request.', response_model=ResourceRequestResponseSchema
)
async def update_resource_request(
    resource_request_id: UUID, body: ResourceRequestUpdateSchema, db_session: AsyncSession = Depends(get_db_session)
) -> ResourceRequestResponseSchema:
    """Update a resource request."""

    resource_request_crud = ResourceRequestCRUD(db_session)

    async with resource_request_crud:
        resource_request = await resource_request_crud.update(resource_request_id, body)

    return resource_request


@router.delete('/{resource_request_id}', summary='Delete a resource request.')
async def delete_resource_request(
    resource_request_id: UUID, db_session: AsyncSession = Depends(get_db_session)
) -> Response:
    """Delete a resource request."""

    resource_request_crud = ResourceRequestCRUD(db_session)

    async with resource_request_crud:
        await resource_request_crud.delete(resource_request_id)

    response = Response(status_code=204)

    return response
