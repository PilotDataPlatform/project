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

from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from project.components.parameters import PageParameters
from project.components.workbench.crud import WorkbenchCRUD
from project.components.workbench.dependencies import get_workbench_crud
from project.components.workbench.schemas import WorkbenchCreateSchema
from project.components.workbench.schemas import WorkbenchListResponseSchema
from project.components.workbench.schemas import WorkbenchResponseSchema
from project.components.workbench.schemas import WorkbenchUpdateSchema

router = APIRouter(prefix='/workbenches', tags=['Workbenches'])


@router.get('/', summary='List all workbenches.', response_model=WorkbenchListResponseSchema)
async def list_workbenches(
    page_parameters: PageParameters = Depends(),
    workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud),
) -> WorkbenchListResponseSchema:
    """List all workbenches."""

    pagination = page_parameters.to_pagination()

    page = await workbench_crud.paginate(pagination)

    response = WorkbenchListResponseSchema.from_page(page)

    return response


@router.get('/{workbench_id}', summary='Get a workbench by id.', response_model=WorkbenchResponseSchema)
async def get_workbench(
    workbench_id: Union[UUID, str], workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)
) -> WorkbenchResponseSchema:
    """Get a workbench by id."""

    workbench = await workbench_crud.retrieve_by_id(workbench_id)

    return workbench


@router.post('/', summary='Create a new workbench.', response_model=WorkbenchResponseSchema)
async def create_workbench(
    body: WorkbenchCreateSchema, workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)
) -> WorkbenchResponseSchema:
    """Create a new workbench."""

    async with workbench_crud:
        workbench = await workbench_crud.create(body)

    return workbench


@router.patch('/{workbench_id}', summary='Update a workbench.', response_model=WorkbenchResponseSchema)
async def update_workbench(
    workbench_id: UUID, body: WorkbenchUpdateSchema, workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)
) -> WorkbenchResponseSchema:
    """Update a workbench."""

    async with workbench_crud:
        workbench = await workbench_crud.update(workbench_id, body)

    return workbench


@router.delete('/{workbench_id}', summary='Delete a workbench.')
async def delete_workbench(workbench_id: UUID, workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)) -> Response:
    """Delete a workbench."""

    async with workbench_crud:
        await workbench_crud.delete(workbench_id)

    response = Response(status_code=204)

    return response
