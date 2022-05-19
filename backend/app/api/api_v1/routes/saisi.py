from select import select
from typing import List
from fastapi import APIRouter, HTTPException, Security, Depends, status, Response
from app.schemas.saisi import SaisiCreate, SaisiOut, SaisiUpdate
from app.core.auth import get_current_active_user
from app.crud.saisi import (
    create_saisi, list_saisi, get_saisi_by_versrubr, 
    get_saisi_by_versfonct, update_saisi, delete_saisi
)
from app.core.auth import get_current_active_user
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db.models import SuiviSaisi, Validation, Saisi,Rubrique, User, VersionOgt
from app.crud.rubrique import get_rubrique_by_intitule
from app.crud.version_ogt import get_version_by_all




router = APIRouter()


@router.post("/saisi/create")
def saisi_create(
    saisi_input: SaisiCreate, intitule: str,rubrique_id : int,versionogt_id : int,
    annee : int, periode: int, typeogt: str, version: str,
    session: Session = Depends(get_db),
    current_user: int = Security(get_current_active_user, scopes=["create_saisi"])
):
  
    idcreate = create_saisi(
            saisi= saisi_input,
            rubrique_id= rubrique_id, versionogt_id=versionogt_id, 
            userc_id=current_user.id, session=session
        )
    db_suivisaisi = SuiviSaisi(saisi_id=idcreate, userc_id=current_user.id)
    db_validation = Validation(saisi_id=idcreate, is_valide=False)
    session.add_all([db_suivisaisi, db_validation])
    session.commit()
    session.refresh(db_suivisaisi)
    session.refresh(db_validation)

    return[db_suivisaisi, db_validation]


@router.get("/saisi/get_all", response_model= List[SaisiOut])
def saisi_list(versionogt_id : int, nature : str, session: Session = Depends(get_db)):

    return get_saisi_by_versfonct(versionogt_id, nature, session)



@router.put("/saisi/update")
def saisi_update(
    saisi_input: SaisiUpdate, intitule: str,
    annee : int, periode: int, typeogt: str, version: str,
    rubrique : int,versionogt : int,
    session: Session = Depends(get_db),
    current_user: int = Security(get_current_active_user, scopes=["update_saisi"])
):

    #rubrique = get_rubrique_by_intitule(intitule=intitule, session=session)
    #versionogt = get_version_by_all(
     #   annee=annee, periode=periode, typeogt=typeogt, version=version, session=session
    #)

    db_saisi = session.query(Saisi).filter(Saisi.versionogt_id==versionogt, Saisi.rubrique_id==rubrique)
    db_validation = session.query(Validation).filter(Validation.saisi_id==db_saisi.first().id)


    idupdate = update_saisi(
            versionogt_id=versionogt,
            rubrique_id=rubrique,
            saisiupdate= saisi_input,
            session=session
        )

    db_suivisaisi = SuiviSaisi(saisi_id=idupdate.id, userc_id=current_user.id)
    session.add(db_suivisaisi)
    session.commit()
    session.refresh(db_suivisaisi)

    return db_suivisaisi

@router.delete("/saisi/delete")
def saisi_delete(
    annee : int, periode: int, typeogt: str, version: str, intitule: str,
    session: Session = Depends(get_db),
    current_user: int = Security(get_current_active_user, scopes=["delete_saisi"])
):
    rubrique = get_rubrique_by_intitule(intitule=intitule, session=session)
    versionogt = get_version_by_all(
        annee=annee, periode=periode, typeogt=typeogt, version=version, session=session
    )

    db_saisi = session.query(Saisi).filter(Saisi.versionogt_id==versionogt.id, Saisi.rubrique_id==rubrique.id)
    db_validation = session.query(Validation).filter(Validation.saisi_id==db_saisi.first().id)

    delete_saisi(
            saisi_id = db_saisi.first().id,
            session=session
        )
        
        