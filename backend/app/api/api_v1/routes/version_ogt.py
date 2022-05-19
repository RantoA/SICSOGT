from fastapi import APIRouter, Request, Depends, Response, encoders
from typing import List

from app.schemas.version_ogt import VersionOgtOut, VersionOgtBase
from app.db.session import get_db
from app.crud.version_ogt import create_new_versionogt, get_all_versionogt, get_one_versionogt, delete_versionogt, update_versionogt


vogt_router = APIRouter()

@vogt_router.post("/versionogt/Create", response_model=VersionOgtOut)
def versionogt_create(versionogts:VersionOgtBase, session_db = Depends(get_db)):
    versionogt_in_db = create_new_versionogt(bd = session_db, vogt = versionogts)

    return versionogt_in_db

@vogt_router.get("/versionogt/get_all")
def versionogt_get(db = Depends(get_db)):
    #get versionogt
    rubrique_in_db = get_all_versionogt(db)

    return rubrique_in_db

@vogt_router.put("/versionogt/update/{versionogt_id}", response_model=VersionOgtOut)
def modif_versionogt(versionogt_id : int, versionogts : VersionOgtBase, db = Depends(get_db)):
    versionogt_in_db = update_versionogt(db = db, vogt_id = versionogt_id, vogt = versionogts)
    return versionogt_in_db

@vogt_router.delete("/versionogt/delete/{version_id}", response_model=VersionOgtOut)
def versionogt_delete(versionogt_id : int, db = Depends(get_db)):
    versionogt_in_db = delete_versionogt(db,versionogt_id)

    return versionogt_in_db




