from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.project.crud import ProjectCRUD
from project.components.project.schemas import ProjectCreateSchema
from project.components.project.schemas import ProjectListResponseSchema
from project.components.project.schemas import ProjectResponseSchema
from project.components.project.schemas import ProjectUpdateSchema
from project.dependencies import get_db_session

router = APIRouter(prefix='/projects', tags=['Projects'])


@router.get('/', summary='List all projects.', response_model=ProjectListResponseSchema)
async def list_projects(db_session: AsyncSession = Depends(get_db_session)) -> ProjectListResponseSchema:
    """List all projects."""

    project_crud = ProjectCRUD(db_session)

    projects = await project_crud.list()

    response = ProjectListResponseSchema(num_of_pages=0, page=0, total=0, result=projects)

    return response


@router.get('/{project_id}', summary='Get a project by id or code.', response_model=ProjectResponseSchema)
async def get_project(
    project_id: Union[UUID, str], db_session: AsyncSession = Depends(get_db_session)
) -> ProjectResponseSchema:
    """Get a project by id or code."""

    project_crud = ProjectCRUD(db_session)

    project = await project_crud.retrieve_by_id_or_code(project_id)

    return project


@router.post('/', summary='Create a new project.', response_model=ProjectResponseSchema)
async def create_project(
    body: ProjectCreateSchema, db_session: AsyncSession = Depends(get_db_session)
) -> ProjectResponseSchema:
    """Create a new project."""

    project_crud = ProjectCRUD(db_session)

    async with project_crud:
        project = await project_crud.create(body)

    return project


@router.patch('/{project_id}', summary='Update a project.', response_model=ProjectResponseSchema)
async def update_project(
    project_id: UUID, body: ProjectUpdateSchema, db_session: AsyncSession = Depends(get_db_session)
) -> ProjectResponseSchema:
    """Update a project."""

    project_crud = ProjectCRUD(db_session)

    async with project_crud:
        project = await project_crud.update(project_id, body)

    return project


@router.delete('/{project_id}', summary='Delete a project.')
async def delete_project(project_id: UUID, db_session: AsyncSession = Depends(get_db_session)) -> Response:
    """Delete a project."""

    project_crud = ProjectCRUD(db_session)

    async with project_crud:
        await project_crud.delete(project_id)

    response = Response(status_code=204)

    return response
