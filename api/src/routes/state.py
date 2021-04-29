from typing import List,Optional
from src.models.state import State
from src.services.state import StateService
from src.models.api_response import ApiResponse
from fastapi import APIRouter,Response,Query,Path

router = APIRouter(prefix='/state',tags=['state'])

responses = {201:{'model':ApiResponse},
    422:{'model':ApiResponse},
    400:{'model':ApiResponse},
    500:{'model':ApiResponse}}

@router.post('/',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=201,responses=responses)
async def post_state(state:State,response:Response):
    try:
        api_response = await StateService.save_state(code=state.code,name=state.name)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e

@router.get('/',response_model=ApiResponse,
    status_code=200,responses=responses)
async def get_state(names:Optional[List[str]] = Query(None,min_length=1),
    limit:Optional[int]=Query(10,ge=1),skip:Optional[int]=Query(0,ge=0)):
    try:
        api_response = await StateService.read_state(names=names,limit=limit,skip=skip)
        return dict(api_response)
    except Exception as e:
        raise e

@router.put('/{id}',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=200,responses=responses)
async def put_state(state:State,response:Response,id:int=Path(...,ge=1)):
    try:
        api_response = await StateService.update_state(id=id,code=state.code,name=state.name)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e

@router.delete('/{id}',response_model=ApiResponse,
    status_code=200,responses=responses)
async def delete_state(response:Response,id:int=Path(...,ge=1)):
    try:
        api_response = await StateService.delete_state(id=id)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e