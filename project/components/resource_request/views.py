from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/resource-requests', tags=['Resource Requests'])


@router.get('/', summary='List all resource requests.')
async def list_resource_requests() -> JSONResponse:
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.get('/{resource_request_id}', summary='Get a resource request by id.')
async def get_resource_request(resource_request_id: str) -> JSONResponse:
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.post('/', summary='Create a new resource request.')
async def create_resource_request() -> JSONResponse:
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.patch('/{resource_request_id}', summary='Update a resource request.')
async def update_resource_request(resource_request_id: str) -> JSONResponse:
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)


@router.delete('/{resource_request_id}', summary='Delete a resource_request.')
async def delete_resource_request(resource_request_id: str) -> JSONResponse:
    return JSONResponse(content={'message': 'Not Implemented'}, status_code=501)
