from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class SaisiBase(BaseModel):
    montant : float
    description : str

class SaisiCreate(SaisiBase):
    pass


class SaisiOrm(SaisiBase):
    version_id : int
    rubrique_id : int
    versionogt_id : int
    user_id : int

    class Config:
        orm_mode=True


class SaisiOut(SaisiBase):
    pass

    class Config:
        orm_mode=True

class SaisiUpdate(SaisiBase):
    pass
