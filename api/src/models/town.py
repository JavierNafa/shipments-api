from typing import Optional
from pydantic import BaseModel,fields

class Town(BaseModel):
    id:Optional[int] = fields.Field(None,ge=1)
    townId:str = fields.Field(min_length=1,max_length=5,regex='^([\s\d]+)$')
    townName:str = fields.Field(min_length=1,max_length=100)
    cityId:str =  fields.Field(None,min_length=1,max_length=5,regex='^([\s\d]+)$')
    cityName:str = fields.Field(None,min_length=1,max_length=100)
    stateId:int = fields.Field(ge=1)