from typing import List
from sqlalchemy.future import select
from fastapi import HTTPException, Query, status, Response
#sans ces imports les tables ne seront pas crées
from app.db.models import Saisi, Rubrique, SuiviSaisi, Validation
from app.schemas.saisi import SaisiCreate, SaisiUpdate




# CREATE
def create_saisi(saisi: SaisiCreate, rubrique_id: int, versionogt_id : int, userc_id: int, session):
    db_saisi = Saisi(
        **saisi.dict(), 
        rubrique_id=rubrique_id, versionogt_id=versionogt_id, userc_id=userc_id
        )  
    session.add(db_saisi)
    session.commit()
    session.refresh(db_saisi)

    return db_saisi.id

# READ
def list_saisi(session):
        
    result = session.execute(select(Saisi))
    return result.scalars().all()

def get_saisi_by_versrubr(version_id: str, rubrique_id: int, session):
        
    result = session.execute(select(Saisi).where(Saisi.versionogt_id==version_id, Saisi.rubrique_id==rubrique_id))
    return result.scalars().first()

def get_saisi_by_versfonct(version_id: int, fonction_id: str, session):
        
    result = session.execute(select(Saisi).join(Rubrique).where(Saisi.versionogt_id==version_id), Rubrique.fonction_id==fonction_id)
    return result.scalars().all()

# UPDATE
def update_saisi(versionogt_id: int, rubrique_id: int, saisiupdate: SaisiUpdate, session):
   
    db_saisi = session.query(Saisi).filter(Saisi.versionogt_id==versionogt_id, Saisi.rubrique_id==rubrique_id)
    
    if not db_saisi.first():
        raise HTTPException(status_code=404, detail="Saisi not found")
    
    db_saisi.update(saisiupdate.dict(), synchronize_session=False)
    session.commit()

    return db_saisi.first()

    
def delete_saisi(saisi_id: int, session):
    #db_saisi = get_saisi_by_versrubr(versionogt_id, rubrique_intitule, session)
    db_suivisaisi = session.query(SuiviSaisi).filter(SuiviSaisi.saisi_id==saisi_id)
    db_validation = session.query(Validation).filter(Validation.saisi_id==saisi_id)
    db_saisi = session.query(Saisi).filter(Saisi.id==saisi_id)
    
    if not db_saisi.first():
        raise HTTPException(status_code=404, detail="Saisi not found")
    db_suivisaisi.delete(synchronize_session=False)
    db_validation.delete(synchronize_session=False)
    db_saisi.delete(synchronize_session=False)
    session.commit()

    return [db_saisi, db_validation, db_suivisaisi]