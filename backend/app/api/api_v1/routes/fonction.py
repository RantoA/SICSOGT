from fastapi import APIRouter, Request, Depends, Response, encoders
from typing import List

from app.schemas.fonction import FonctionCreate,FonctionBase, FonctionOut
from app.db.session import get_db
from app.crud.fonction import get_fonction, create_fonction, delete_fonction, update_fonction


fonction_router = APIRouter()

@fonction_router.post("/fonction/Create", response_model=FonctionOut)
def fonction_create(fonction:FonctionCreate, db = Depends(get_db)):
    fonction_in_db = create_fonction(fonction = fonction, db = db)

    return fonction_in_db

@fonction_router.get("/fonction/get_all", response_model=List[FonctionOut])
def fonction_get(db = Depends(get_db)):
    #get fonction
    fonction_in_db = get_fonction(db)

    return fonction_in_db

@fonction_router.put("/fonction/update/{fonction_id}", response_model=FonctionOut)
def modif_fonction(fonction_id : int, fonction : FonctionCreate, db = Depends(get_db)):
    resultat_db = update_fonction(db = db, fonction_id = fonction_id, fonction=fonction)
    return resultat_db

@fonction_router.delete("/fonction/delete/{fonction_id}", response_model=FonctionOut)
def fonction_delete(fonction_id : int, db = Depends(get_db)):
    fonction_in_db = delete_fonction(db,fonction_id)

    return fonction_in_db




