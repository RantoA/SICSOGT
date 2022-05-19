from typing import Optional
from pydantic import BaseModel

class OgtBase(BaseModel):
    intitule : str
    abrev : str
    niveau : int
    description : Optional[str]
    userc_id : int

    class Config:
        orm_mode = True
class OgtOut(OgtBase):
    id : int
       
    class Config:
        orm_mode = True

