from typing import Optional
from pydantic import BaseModel


# Shared properties
class VersionOgtBase(BaseModel):
    annee: int
    periode : int
    typeogt : str
    version : str
    description : Optional[str]
    userc_id : int

class VersionOgtOut(VersionOgtBase):
    id : int
    class Config:
        orm_mode = True   

