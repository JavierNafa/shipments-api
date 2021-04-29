from typing import List,Optional
from src.models.suburb import Suburb
from src.services.suburb import SuburbService
from src.models.api_response import ApiResponse
from fastapi import APIRouter,Response,Query,Path

router = APIRouter(prefix='/suburb',tags=['suburb'])

responses = {201:{'model':ApiResponse},
    422:{'model':ApiResponse},
    400:{'model':ApiResponse},
    500:{'model':ApiResponse}}

@router.post('/',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=201,responses=responses)
async def post_suburb(suburb:Suburb,response:Response):
    try:
        api_response = await SuburbService.save_suburb(unique_suburb_town_id=suburb.uniqueSuburbTownId,
                name=suburb.name,postal_code=suburb.postalCode,postal_code_administration=suburb.postalCodeAdministration,
                postal_code_office=suburb.postalCodeOffice,cp=suburb.cp,code_type=suburb.codeType,
                type_=suburb.type_,zone=suburb.zone,town_id=suburb.townId)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e

@router.get('/',response_model=ApiResponse,
    status_code=200,responses=responses)
async def get_suburb(postalCodes:Optional[List[int]] = Query(None),
    names:Optional[List[str]] = Query(None,min_length=1),
    limit:Optional[int]=Query(10,ge=1),skip:Optional[int]=Query(0,ge=0)):
    try:
        api_response = await SuburbService.read_suburb(postal_codes=postalCodes,names=names,limit=limit,skip=skip)
        return dict(api_response)
    except Exception as e:
        raise e

@router.put('/{id}',response_model=ApiResponse,
    response_model_exclude={'id'},
    status_code=200,responses=responses)
async def put_suburb(suburb:Suburb,response:Response,id:int=Path(...,ge=1)):
    try:
        api_response = await SuburbService.update_suburb(id=id,unique_suburb_town_id=suburb.uniqueSuburbTownId,
                name=suburb.name,postal_code=suburb.postalCode,postal_code_administration=suburb.postalCodeAdministration,
                postal_code_office=suburb.postalCodeOffice,cp=suburb.cp,code_type=suburb.codeType,
                type_=suburb.type_,zone=suburb.zone,town_id=suburb.townId)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e

@router.delete('/{id}',response_model=ApiResponse,
    status_code=200,responses=responses)
async def delete_suburb(response:Response,id:int=Path(...,ge=1)):
    try:
        api_response = await SuburbService.delete_suburb(id=id)
        response.status_code = api_response.statusCode
        return dict(api_response)
    except Exception as e:
        raise e