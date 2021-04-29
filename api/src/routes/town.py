from typing import List,Optional
from src.models.town import Town
from src.services.town import TownService
from src.models.api_response import ApiResponse
from fastapi import APIRouter,Response,Query,Path

router = APIRouter(prefix='/town',tags=['town'])

responses = {201:{'model':ApiResponse},
    422:{'model':ApiResponse},
    400:{'model':ApiResponse},
    500:{'model':ApiResponse}}

@router.post('/',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=201,responses=responses)
async def post_town(town:Town,response:Response):
    try:
        api_response = await TownService.save_town(town_id=town.townId,
                town_name=town.townName,city_id=town.cityId,city_name=town.cityName,state_id=town.stateId)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e

@router.get('/',response_model=ApiResponse,
    status_code=200,responses=responses)
async def get_town(townNames:Optional[List[str]] = Query(None,min_length=1),
    cityNames:Optional[List[str]] = Query(None,min_length=1),
    limit:Optional[int]=Query(10,ge=1),skip:Optional[int]=Query(0,ge=0)):
    try:
        api_response = await TownService.read_town(town_names=townNames,city_names=cityNames,limit=limit,skip=skip)
        return dict(api_response)
    except Exception as e:
        raise e

@router.put('/{id}',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=200,responses=responses)
async def put_town(town:Town,response:Response,id:int=Path(...,ge=1)):
    try:
        api_response = await TownService.update_town(id=id,town_id=town.townId,
                town_name=town.townName,city_id=town.cityId,city_name=town.cityName,state_id=town.stateId)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e

@router.delete('/{id}',response_model=ApiResponse,
    status_code=200,responses=responses)
async def delete_town(response:Response,id:int=Path(...,ge=1)):
    try:
        api_response = await TownService.delete_town(id=id)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e