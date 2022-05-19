from sqlalchemy.future import select
from http.client import HTTPException
from sqlalchemy.orm import Session

from app.db.models import VersionOgt
from app.schemas.version_ogt import VersionOgtBase


def get_all_versionogt(db : Session):
    reponse_db = db.query(VersionOgt).filter().all()
    return reponse_db

def get_one_versionogt(db : Session, versionogt_id : int):
    reponse_db = db.query(VersionOgt).filter(VersionOgt.id==versionogt_id).first()

    if not reponse_db:
        raise HTTPException(status_code=404, detail="Version ogt not found")
    
    return reponse_db

def create_new_versionogt(bd : Session, vogt : VersionOgtBase):
    rubrique_db = VersionOgt(annee = vogt.annee,
                             periode = vogt.periode,
                             typeogt = vogt.typeogt,
                             version = vogt.version,
                             description = vogt.description.capitalize(),
                             userc_id = vogt.userc_id)
    
    bd.add(rubrique_db)
    bd.commit()
    bd.refresh(rubrique_db)

    return rubrique_db

def delete_versionogt(db : Session, vogt_id : int):
    vogt_in_db = get_one_versionogt(db, vogt_id)

    if not vogt_in_db:
        raise HTTPException(status_code=404, detail="Version ogt not found")
    
    db.delete(vogt_in_db)
    db.commit()

    return vogt_in_db

def update_versionogt(db : Session, vogt_id : int, vogt : VersionOgtBase):
    reponse_in_db = get_one_versionogt(db, vogt_id)

    if not reponse_in_db:
        raise HTTPException(status_code=404, detail="Version ogtvogt not found")
    
    reponse_in_db.annee = vogt.annee
    reponse_in_db.periode = vogt.periode
    reponse_in_db.typeogt = vogt.typeogt
    reponse_in_db.version = vogt.version
    reponse_in_db.description = vogt.description.capitalize()
    reponse_in_db.userc_id = vogt.userc_id

    db.commit()
    db.refresh(reponse_in_db)

    return reponse_in_db

def get_version_by_all(annee: int, periode: int, typeogt: str, version: str, session):
        
    result = session.execute(select(VersionOgt).where(
        VersionOgt.annee==annee,
        VersionOgt.periode==periode,
        VersionOgt.typeogt==typeogt,
        VersionOgt.version==version
        ))
        
    return result.scalars().first()
   
