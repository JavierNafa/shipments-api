from src.models.api_response import ApiResponse
from src.repositories.suburb import SuburbRepository

class SuburbService:

    @staticmethod
    async def save_suburb(unique_suburb_town_id:str,name:str,postal_code:int,postal_code_administration:int,postal_code_office:int,
        cp:str,code_type:str,type_:str,zone:str,town_id:int):
        try:
            result = await SuburbRepository.create(unique_suburb_town_id=unique_suburb_town_id,
                name=name,postal_code=postal_code,postal_code_administration=postal_code_administration,
                postal_code_office=postal_code_office,cp=cp,code_type=code_type,type_=type_,zone=zone,town_id=town_id)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e
    
    @staticmethod
    async def read_suburb(postal_codes:list,names:list,limit:int,skip:int):
        try:
            result = await SuburbRepository.read(postal_codes=postal_codes,names=names,limit=limit,skip=skip)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e

    @staticmethod
    async def update_suburb(id:int,unique_suburb_town_id:str,name:str,postal_code:int,postal_code_administration:int,postal_code_office:int,
        cp:str,code_type:str,type_:str,zone:str,town_id:int):
        try:
            result = await SuburbRepository.update(id=id,unique_suburb_town_id=unique_suburb_town_id,
                name=name,postal_code=postal_code,postal_code_administration=postal_code_administration,
                postal_code_office=postal_code_office,cp=cp,code_type=code_type,type_=type_,zone=zone,town_id=town_id)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e

    @staticmethod
    async def delete_suburb(id:int):
        try:
            result = await SuburbRepository.delete(id=id)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e