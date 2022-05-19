import typing as t

from pydantic import BaseModel


# Shared properties
class FonctionBase(BaseModel):
    nature: str
    description : t.Optional[str]
    


# Properties to receive via API on creation
class FonctionCreate(FonctionBase):
    pass

class FonctionOut(FonctionCreate):
    id : int
    class Config:
        orm_mode = True   
class FonctionEdit(FonctionBase):

    class Config:
        orm_mode = True
