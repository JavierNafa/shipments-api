from typing import Optional
from pydantic import BaseModel,fields

class User(BaseModel):
    id:Optional[int] = fields.Field(None,ge=1)
    name:str = fields.Field(min_length=1,max_length=100)
    lastName:str = fields.Field(min_length=1,max_length=100)
    username:str =  fields.Field(min_length=1,max_length=150)
    password:str = fields.Field(min_length=8,max_length=100)