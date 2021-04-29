from typing import Any
from pydantic import BaseModel,fields

class ApiResponse(BaseModel):
    message:str
    data:Any = fields.Field(None)
    success:bool = fields.Field(False)
    statusCode:int = fields.Field(400)

    def __iter__(self):
        yield from {
            'message': self.message,
            'data': self.data,
            'success':self.success,
            'statusCode':self.statusCode
        }.items()