from sqlalchemy.future import select
from http.client import HTTPException
from sqlalchemy.orm import Session, session

from app.db.models import Rubrique
from app.schemas.rubrique import RubriqueBase


def get_all_rubrique(db : Session):
    reponse_db = db.query(Rubrique).filter().all()
    return reponse_db

def get_one_rubrique(db : Session, rubrique_id : int):
    reponse_db = db.query(Rubrique).filter(Rubrique.id==rubrique_id).first()

    if not reponse_db:
        raise HTTPException(status_code=404, detail="Rubrique not found")
    
    return reponse_db

def create_new_rubric(bd : session, rubrics : RubriqueBase):
    rubrique_db = Rubrique(intitule = rubrics.intitule.title(),
                           abrev = rubrics.abrev.upper(),
                           niveau_saisi = rubrics.niveau_saisi,
                           niveau_sorti = rubrics.niveau_sorti,
                           description = rubrics.description.capitalize(),
                           fonction_id = rubrics.fonction_id,
                           ogt_id = rubrics.ogt_id,
                           userc_id = rubrics.userc_id)
    
    bd.add(rubrique_db)
    bd.commit()
    bd.refresh(rubrique_db)

    return rubrique_db

def delete_rubrique(db : Session, rub_id : int):
    rub_in_db = get_one_rubrique(db, rub_id)

    if not rub_in_db:
        raise HTTPException(status_code=404, detail="Rubrique not found")
    
    db.delete(rub_in_db)
    db.commit()

    return rub_in_db

def update_rubrique(db : Session, rub_id : int, rubrics : RubriqueBase):
    rub_in_db = get_one_rubrique(db, rub_id)

    if not rub_in_db:
        raise HTTPException(status_code=404, detail="Rubrique not found")
    
    rub_in_db.intitule = rubrics.intitule
    rub_in_db.abrev = rubrics.abrev
    rub_in_db.niveau_saisi = rubrics.niveau_saisi
    rub_in_db.niveau_sorti = rubrics.niveau_sorti
    rub_in_db.descriotion = rubrics.description
    rub_in_db.fonction_id = rubrics.fonction_id
    rub_in_db.ogt_id = rubrics.ogt_id
    rub_in_db.userc_id = rubrics.userc_id

    db.commit()
    db.refresh(rub_in_db)

    return rub_in_db


def get_rubrique_by_intitule(intitule: str, session):
        
    result = session.execute(select(Rubrique).where(Rubrique.intitule==intitule))
    return result.scalars().first()
