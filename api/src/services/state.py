from src.models.api_response import ApiResponse
from src.repositories.state import StateRepository

class StateService:

    @staticmethod
    async def save_state(code:str,name:str):
        try:
            result = await StateRepository.create(code=code,name=name)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e
    
    @staticmethod
    async def read_state(names:list,limit:int,skip:int):
        try:
            result = await StateRepository.read(names=names,limit=limit,skip=skip)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e

    @staticmethod
    async def update_state(id:int,code:str,name:str):
        try:
            result = await StateRepository.update(id=id,code=code,name=name)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e

    @staticmethod
    async def delete_state(id:int):
        try:
            result = await StateRepository.delete(id=id)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e