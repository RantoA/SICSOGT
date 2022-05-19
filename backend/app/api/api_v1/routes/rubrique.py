from fastapi import APIRouter, Request, Depends, Response, encoders
from typing import List

from app.schemas.rubrique import RubriqueBase,RubriqueOut
from app.db.session import get_db
from app.crud.rubrique import create_new_rubric, update_rubrique, delete_rubrique, get_all_rubrique, get_one_rubrique


rb_router = APIRouter()

@rb_router.post("/rubrique/Create", response_model=RubriqueOut)
def rubrique_create(rubriques:RubriqueBase, session_db = Depends(get_db)):
    rubrique_in_db = create_new_rubric(bd = session_db, rubrics = rubriques)

    return rubrique_in_db

@rb_router.get("/rubrique/get_all")
def ribrique_get(db = Depends(get_db)):
    #get rubrique
    rubrique_in_db = get_all_rubrique(db)

    return rubrique_in_db

@rb_router.put("/rubrique/update/{rubrique_id}", response_model=RubriqueOut)
def modif_rubrique(rubrique_id : int, rubrique : RubriqueBase, db = Depends(get_db)):
    rubrique_in_db = update_rubrique(db = db, rub_id = rubrique_id, rubrics = rubrique)
    return rubrique_in_db

@rb_router.delete("/rubrique/delete/{rubrique_id}", response_model=RubriqueOut)
def rubrique_delete(rubrique_id : int, db = Depends(get_db)):
    rubrique_in_db = delete_rubrique(db,rubrique_id)

    return rubrique_in_db




