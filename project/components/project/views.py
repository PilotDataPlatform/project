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
from project.components.parameters import SortParameters
from project.components.project.crud import ProjectCRUD
from project.components.project.dependencies import get_logo_uploader
from project.components.project.dependencies import get_project_crud
from project.components.project.logo_uploader import LogoUploader
from project.components.project.parameters import ProjectFilterParameters
from project.components.project.parameters import ProjectSortByFields
from project.components.project.schemas import ProjectCreateSchema
from project.components.project.schemas import ProjectListResponseSchema
from project.components.project.schemas import ProjectLogoUploadSchema
from project.components.project.schemas import ProjectResponseSchema
from project.components.project.schemas import ProjectUpdateSchema

router = APIRouter(prefix='/projects', tags=['Projects'])


@router.get('/', summary='List all projects.', response_model=ProjectListResponseSchema)
async def list_projects(
    filter_parameters: ProjectFilterParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(ProjectSortByFields) = Depends(),
    page_parameters: PageParameters = Depends(),
    project_crud: ProjectCRUD = Depends(get_project_crud),
) -> ProjectListResponseSchema:
    """List all projects."""

    filtering = filter_parameters.to_filtering()
    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()

    async with project_crud:
        page = await project_crud.paginate(pagination, sorting, filtering)

    response = ProjectListResponseSchema.from_page(page)

    return response


@router.get('/{project_id}', summary='Get a project by id or code.', response_model=ProjectResponseSchema)
async def get_project(
    project_id: Union[UUID, str], project_crud: ProjectCRUD = Depends(get_project_crud)
) -> ProjectResponseSchema:
    """Get a project by id or code."""

    async with project_crud:
        project = await project_crud.retrieve_by_id_or_code(project_id)

    return project


@router.post('/', summary='Create a new project.', response_model=ProjectResponseSchema)
async def create_project(
    body: ProjectCreateSchema, project_crud: ProjectCRUD = Depends(get_project_crud)
) -> ProjectResponseSchema:
    """Create a new project."""

    async with project_crud:
        project = await project_crud.create(body)

    return project


@router.patch('/{project_id}', summary='Update a project.', response_model=ProjectResponseSchema)
async def update_project(
    project_id: UUID, body: ProjectUpdateSchema, project_crud: ProjectCRUD = Depends(get_project_crud)
) -> ProjectResponseSchema:
    """Update a project."""

    async with project_crud:
        project = await project_crud.update(project_id, body)

    return project


@router.delete('/{project_id}', summary='Delete a project.')
async def delete_project(project_id: UUID, project_crud: ProjectCRUD = Depends(get_project_crud)) -> Response:
    """Delete a project."""

    async with project_crud:
        await project_crud.delete(project_id)

    response = Response(status_code=204)

    return response


@router.post('/{project_id}/logo', summary='Upload a logo for a project.', response_model=ProjectResponseSchema)
async def upload_project_logo(
    project_id: UUID,
    body: ProjectLogoUploadSchema,
    project_crud: ProjectCRUD = Depends(get_project_crud),
    logo_uploader: LogoUploader = Depends(get_logo_uploader),
) -> ProjectResponseSchema:
    """Upload a logo for a project."""

    async with project_crud:
        await project_crud.retrieve_by_id(project_id)

    image = body.get_image()
    logo_name = f'{project_id}.png'

    await logo_uploader.convert_and_upload(image, logo_name)

    async with project_crud:
        project_update = ProjectUpdateSchema(logo_name=logo_name)
        project = await project_crud.update(project_id, project_update)

    return project
