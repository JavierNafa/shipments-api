from typing import Optional
from pydantic import BaseModel,fields

class State(BaseModel):
    id:Optional[int] = fields.Field(None,ge=1)
    code:str = fields.Field(min_length=1,max_length=20,regex='^([\s\d]+)$')
    name:str = fields.Field(min_length=1,max_length=20)