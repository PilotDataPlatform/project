from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/projects', tags=['Projects'])


@router.get('/', summary='List all projects.')
async def list_projects():
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.get('/{project_id}', summary='Get a project by id or code.')
async def get_project(project_id: str):
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.post('/', summary='Create a new project.')
async def create_project():
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.patch('/{project_id}', summary='Update a project.')
async def update_project(project_id: str):
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.delete('/{project_id}', summary='Delete a project.')
async def delete_project(project_id: str):
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)
