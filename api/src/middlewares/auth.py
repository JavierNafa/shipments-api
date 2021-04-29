import ast
from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from src.models.api_response import ApiResponse
from src.services.account import AccountService
from src.utils.token_generator import decode_token

async def verify_token(request:Request):
    try:
        authorization = request.headers.get('Authorization',None)
        if authorization:
            _, token = authorization.split(' ')
            decoded = decode_token(token)
            if decoded:
                return True
        raise HTTPException(
                status_code=403,
                detail="Invalid token"
            )
    except Exception as e:
        raise e