from typing import List,Optional
from src.models.user import User
from src.services.account import AccountService
from src.models.api_response import ApiResponse
from fastapi import APIRouter,Response,Query,Path,Body

router = APIRouter(prefix='/account',tags=['account'])

responses = {201:{'model':ApiResponse},
    422:{'model':ApiResponse},
    400:{'model':ApiResponse},
    500:{'model':ApiResponse}}

@router.post('/register',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=201,responses=responses)
async def post_account(user:User,response:Response):
    try:
        api_response = await AccountService.register(name=user.name,last_name=user.lastName,
            username=user.username,password=user.password)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e

@router.post('/login',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=200,responses=responses)
async def post_account(response:Response,username:str=Body(...,min_length=1,max_length=150),
    password:str=Body(...,min_length=8,max_length=100)):
    try:
        api_response = await AccountService.login(username=username,password=password)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e