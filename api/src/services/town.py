from src.models.api_response import ApiResponse
from src.repositories.town import TownRepository

class TownService:

    @staticmethod
    async def save_town(town_id:str,town_name:str,city_id:str,city_name:str,state_id:int):
        try:
            result = await TownRepository.create(town_id=town_id,
                town_name=town_name,city_id=city_id,city_name=city_name,state_id=state_id)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e
    
    @staticmethod
    async def read_town(town_names:list,city_names:list,limit:int,skip:int):
        try:
            result = await TownRepository.read(town_names=town_names,city_names=city_names,limit=limit,skip=skip)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e

    @staticmethod
    async def update_town(id:int,town_id:str,town_name:str,city_id:str,city_name:str,state_id:int):
        try:
            result = await TownRepository.update(id=id,town_id=town_id,
                town_name=town_name,city_id=city_id,city_name=city_name,state_id=state_id)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e

    @staticmethod
    async def delete_town(id:int):
        try:
            result = await TownRepository.delete(id=id)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e