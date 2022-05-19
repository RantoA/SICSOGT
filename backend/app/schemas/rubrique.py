from typing import Optional
from pydantic import BaseModel

class RubriqueBase(BaseModel):
    intitule : str
    abrev : str
    niveau_saisi : int
    niveau_sorti : int
    description : Optional[str]
    fonction_id : int
    userc_id : int
    ogt_id : int
    

    class Config:
        orm_mode = True
class RubriqueOut(RubriqueBase):
    id : int
       
    class Config:
        orm_mode = True

