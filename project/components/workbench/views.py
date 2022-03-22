from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/workbenches', tags=['Workbenches'])


@router.get('/', summary='List all workbenches.')
async def list_workbenches():
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.get('/{workbench_id}', summary='Get a workbench by id.')
async def get_workbench(workbench_id: str):
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.post('/', summary='Create a new workbench.')
async def create_workbench():
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.patch('/{workbench_id}', summary='Update a workbench.')
async def update_workbench(workbench_id: str):
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.delete('/{workbench_id}', summary='Delete a workbench.')
async def delete_workbench(workbench_id: str):
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)
