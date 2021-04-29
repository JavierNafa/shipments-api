import base64
from src.models.api_response import ApiResponse
from src.repositories.user import UserRepository
from src.utils.hash_generator import encode_hash,decode_hash
from src.utils.token_generator import encode_token,decode_token

class AccountService:

    @staticmethod
    async def register(name:str,last_name:str,username:str,password:str):
        try:
            encoded_password = encode_hash(payload=password)
            result = await UserRepository.create(name=name,last_name=last_name,username=username,password=encoded_password)
            success,message,status_code,data = result.values()
            api_response = ApiResponse(message=message,data=data,success=success,statusCode=status_code)
            return api_response
        except Exception as e:
            raise e
    
    @staticmethod
    async def login(username:str,password:str):
        try:
            result = await UserRepository.read(username=username)
            success,message,status_code,data = result.values()
            if success:
                encoded_password = base64.b64decode(data['password'])
                is_valid = decode_hash(payload=password,hash_storage=encoded_password)
                if is_valid:
                    token = encode_token(username=username)
                    api_response = ApiResponse(message='OK',data=token,success=True,statusCode=200)
                    return api_response
            api_response = ApiResponse(message='Incorrect credentials',data=None,success=False,statusCode=401)
            return api_response
        except Exception as e:
            raise e
    
    @staticmethod
    async def check_user(username:str):
        try:
            result = await UserRepository.read(username=username)
            success,message,status_code,data = result.values()
            return success,status_code,message
        except Exception as e:
            raise e