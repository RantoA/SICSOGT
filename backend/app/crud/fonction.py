import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import typing as t

from app.schemas.fonction import FonctionBase, FonctionCreate
from app.core.security import get_password_hash

from app.db.models import Fonction

def get_fonction_by_id(db: Session, id: int) -> FonctionCreate:
    return db.query(Fonction).filter(Fonction.id == id).first()

def get_fonction(session : Session):
    fonction = session.query(Fonction).filter().all()
    return fonction


def create_fonction(db : Session, fonction : FonctionCreate):
  
    fonction_in_db = Fonction(nature = fonction.nature.title(), 
                              description = fonction.description.capitalize())

    db.add(fonction_in_db)
    db.commit()
    db.refresh(fonction_in_db)

    return fonction_in_db

def update_fonction(db: Session, fonction_id: int, fonction:FonctionCreate):
    db_finction= get_fonction_by_id(db, fonction_id)

    if not get_fonction:
        raise HTTPException(status=404, detail="fonction not found")
    

    db_finction.nature=fonction.nature.title()
    db_finction.description=fonction.description.capitalize()
 
    db.commit()
    db.refresh(db_finction)

    return db_finction


def delete_fonction(session : Session, fonction_id : int):
    reponse_db = get_fonction_by_id(session,fonction_id)

    if not reponse_db:
        raise HTTPException(status_code=404, detail="fonction not found")
    session.delete(reponse_db)
    session.commit()

    return reponse_db