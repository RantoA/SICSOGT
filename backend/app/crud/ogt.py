from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Ogt
from app.schemas.ogt import OgtBase

def get_one_ogt(session : Session, ogt_id : int):
    reponse_db = session.query(Ogt).filter(Ogt.id==ogt_id).first()
    return reponse_db

def get_all_ogt(session : Session):
    reponse_db = session.query(Ogt).filter().all()
    return reponse_db

def create_ogt(db : Session, ogt : OgtBase):
    reponse = Ogt(intitule=ogt.intitule.title(),
                     abrev=ogt.abrev.upper(),
                     niveau=ogt.niveau,
                     description=ogt.description.capitalize(),
                     userc_id=ogt.userc_id)
    db.add(reponse)
    db.commit()
    db.refresh(reponse)

    return reponse

def delete_ogt(session : Session, ogt_id : int):
    reponse = get_one_ogt(session,ogt_id)
    if not reponse:
        raise HTTPException(status_code=404, detail="Ogt not found")
    session.delete(reponse)
    session.commit()

    return reponse

def update_ogt(db: Session, ogt_id: int, ogt:OgtBase):
    reponse_db = get_one_ogt(db, ogt_id)
    if not reponse_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ogt not found")
    
    reponse_db.intitule = ogt.intitule.title()
    reponse_db.abrev = ogt.abrev.upper()
    reponse_db.niveau = ogt.niveau
    reponse_db.description = ogt.description.capitalize()
    reponse_db.userc_id = ogt.userc_id
    
    db.commit()
    db.refresh(reponse_db)
    return reponse_db




