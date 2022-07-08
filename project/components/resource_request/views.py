# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from project.components.parameters import PageParameters
from project.components.parameters import SortParameters
from project.components.resource_request.crud import ResourceRequestCRUD
from project.components.resource_request.dependencies import get_resource_request_crud
from project.components.resource_request.parameters import ResourceRequestSortByFields
from project.components.resource_request.schemas import ResourceRequestCreateSchema
from project.components.resource_request.schemas import ResourceRequestListResponseSchema
from project.components.resource_request.schemas import ResourceRequestResponseSchema
from project.components.resource_request.schemas import ResourceRequestUpdateSchema

router = APIRouter(prefix='/resource-requests', tags=['Resource Requests'])


@router.get('/', summary='List all resource requests.', response_model=ResourceRequestListResponseSchema)
async def list_resource_requests(
    page_parameters: PageParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(ResourceRequestSortByFields) = Depends(),
    resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud),
) -> ResourceRequestListResponseSchema:
    """List all resource requests."""

    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()

    page = await resource_request_crud.paginate(pagination, sorting)

    response = ResourceRequestListResponseSchema.from_page(page)

    return response


@router.get(
    '/{resource_request_id}',
    summary='Get a resource request by id.',
    response_model=ResourceRequestResponseSchema,
)
async def get_resource_request(
    resource_request_id: UUID, resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud)
) -> ResourceRequestResponseSchema:
    """Get a resource request by id."""

    resource_request = await resource_request_crud.retrieve_by_id(resource_request_id)
    return resource_request


@router.post('/', summary='Create a new resource request.', response_model=ResourceRequestResponseSchema)
async def create_resource_request(
    body: ResourceRequestCreateSchema, resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud)
) -> ResourceRequestResponseSchema:
    """Create a new resource request."""

    async with resource_request_crud:
        resource_request = await resource_request_crud.create(body)

    return resource_request


@router.patch(
    '/{resource_request_id}', summary='Update a resource request.', response_model=ResourceRequestResponseSchema
)
async def update_resource_request(
    resource_request_id: UUID,
    body: ResourceRequestUpdateSchema,
    resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud),
) -> ResourceRequestResponseSchema:
    """Update a resource request."""

    async with resource_request_crud:
        resource_request = await resource_request_crud.update(resource_request_id, body)

    return resource_request


@router.delete('/{resource_request_id}', summary='Delete a resource request.')
async def delete_resource_request(
    resource_request_id: UUID, resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud)
) -> Response:
    """Delete a resource request."""

    async with resource_request_crud:
        await resource_request_crud.delete(resource_request_id)

    response = Response(status_code=204)

    return response
