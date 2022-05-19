from app.schemas.ogt import OgtBase, OgtOut
from fastapi import APIRouter, Request, Depends, Response, encoders
from typing import List

from app.db.session import get_db
from app.crud.ogt import get_all_ogt, delete_ogt, create_ogt, update_ogt


ogt_router = APIRouter()

@ogt_router.post("/ogt/create", response_model=OgtBase)
def fonction_create(ogt: OgtBase, db = Depends(get_db)):
    ogt_in_db = create_ogt(db,ogt)

    return ogt_in_db

@ogt_router.get("/ogt/get_all")
def ogt_get(db = Depends(get_db)):
    #get ogt
    ogt_in_db = get_all_ogt(db)

    return ogt_in_db

@ogt_router.put("/ogt/update/{ogt_id}", response_model=OgtBase)
def modif_fogt(ogt_id : int, ogt : OgtBase, db = Depends(get_db)):
    resultat_db = update_ogt(db = db, ogt_id = ogt_id, ogt=ogt)
    return resultat_db

@ogt_router.delete("/ogt/delete/{ogt_id}", response_model=OgtOut)
def ogt_delete(ogt_id : int, db = Depends(get_db)):
    ogt_in_db = delete_ogt(db,ogt_id)

    return ogt_in_db



