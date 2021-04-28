from typing import Optional
from src.models.zone import Zone
from pydantic import BaseModel,fields
from src.models.suburb_type import SuburbType

class Suburb(BaseModel):
    id:Optional[int] = fields.Field(None,ge=0)
    uniqueSuburbTownId:str = fields.Field(min_length=1,max_length=100,regex='^([\s\d]+)$')
    name:str = fields.Field(min_length=1,max_length=50)
    postalCode:int = fields.Field(ge=10000,le=99999)
    postalCodeAdministration:int = fields.Field(ge=10000,le=99999)
    postalCodeOffice:int = fields.Field(ge=10000,le=99999)
    cp:Optional[str] = fields.Field(None,min_length=1)
    codeType:str = fields.Field(min_length=1,max_length=5)
    type_:SuburbType
    zone:Zone
    townId:int = fields.Field(ge=1)