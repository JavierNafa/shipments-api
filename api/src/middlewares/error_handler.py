from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from src.models.api_response import ApiResponse
from fastapi.exceptions import RequestValidationError,StarletteHTTPException

class ErrorHandler():

    @staticmethod
    async def handle_error(request,e):
        if isinstance(e,RequestValidationError):
            error,*remain = e.errors()
            location,message,*extra = error.values()
            api_response = ApiResponse(message=message,data=location,success=False,statusCode=422)
            json_response = JSONResponse(content=dict(api_response),status_code=api_response.statusCode)
            return json_response
        elif isinstance(e,SQLAlchemyError):
            api_response = ApiResponse(message=e._message(),data=None,success=False,statusCode=500)
            json_response = JSONResponse(content=dict(api_response),status_code=api_response.statusCode)
            return json_response
        elif isinstance(e,StarletteHTTPException):
            api_response = ApiResponse(message=e.detail,data=None,success=False,statusCode=e.status_code)
            json_response = JSONResponse(content=dict(api_response),status_code=api_response.statusCode)
            return json_response
        api_response = ApiResponse(message=f'Unexpected error: {e}',data=None,success=False,statusCode=500)
        json_response = JSONResponse(content=dict(api_response),status_code=api_response.statusCode)
        return json_response