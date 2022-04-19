from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.workbench.crud import WorkbenchCRUD
from project.components.workbench.schemas import WorkbenchCreateSchema
from project.components.workbench.schemas import WorkbenchListResponseSchema
from project.components.workbench.schemas import WorkbenchResponseSchema
from project.components.workbench.schemas import WorkbenchUpdateSchema
from project.dependencies import get_db_session

router = APIRouter(prefix='/workbenches', tags=['Workbenches'])


@router.get('/', summary='List all workbenches.', response_model=WorkbenchListResponseSchema)
async def list_workbenches(db_session: AsyncSession = Depends(get_db_session)) -> WorkbenchListResponseSchema:
    """List all workbenches."""

    workbench_crud = WorkbenchCRUD(db_session)

    workbenches = await workbench_crud.list()

    response = WorkbenchListResponseSchema(num_of_pages=0, page=0, total=0, result=workbenches)

    return response


@router.get('/{workbench_id}', summary='Get a workbench by id.', response_model=WorkbenchResponseSchema)
async def get_workbench(
    workbench_id: Union[UUID, str], db_session: AsyncSession = Depends(get_db_session)
) -> WorkbenchResponseSchema:
    """Get a workbench by id."""

    workbench_crud = WorkbenchCRUD(db_session)

    workbench = await workbench_crud.retrieve_by_id(workbench_id)

    return workbench


@router.post('/', summary='Create a new workbench.', response_model=WorkbenchResponseSchema)
async def create_workbench(
    body: WorkbenchCreateSchema, db_session: AsyncSession = Depends(get_db_session)
) -> WorkbenchResponseSchema:
    """Create a new workbench."""

    workbench_crud = WorkbenchCRUD(db_session)

    async with workbench_crud:
        workbench = await workbench_crud.create(body)

    return workbench


@router.patch('/{workbench_id}', summary='Update a workbench.', response_model=WorkbenchResponseSchema)
async def update_workbench(
    workbench_id: UUID, body: WorkbenchUpdateSchema, db_session: AsyncSession = Depends(get_db_session)
) -> WorkbenchResponseSchema:
    """Update a workbench."""

    workbench_crud = WorkbenchCRUD(db_session)

    async with workbench_crud:
        workbench = await workbench_crud.update(workbench_id, body)

    return workbench


@router.delete('/{workbench_id}', summary='Delete a workbench.')
async def delete_workbench(workbench_id: UUID, db_session: AsyncSession = Depends(get_db_session)) -> Response:
    """Delete a workbench."""

    workbench_crud = WorkbenchCRUD(db_session)

    async with workbench_crud:
        await workbench_crud.delete(workbench_id)

    response = Response(status_code=204)

    return response
