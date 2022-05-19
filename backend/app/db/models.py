from datetime import datetime
from enum import unique

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlalchemy import (
    Column, DateTime, Integer, String, Boolean, Float, ForeignKey
    )
from sqlalchemy.orm import declarative_mixin, relationship

from app.db.session import Base


@declarative_mixin
class TimesCreate:
    #datecreate = Column(DateTime, default=datetime.now, nullable=False)
    datecreate=Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

@declarative_mixin
class TimesUpdate:
    #dateupdate = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    dateupdate=Column(TIMESTAMP(timezone=True),
                        nullable=False, onupdate=datetime.now, server_default=text('now()'))
    

class Fonction(TimesCreate, TimesUpdate, Base):
    __tablename__ = 'fonctions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nature = Column(String(50), nullable=False, unique= True)
    description = Column(String(50), nullable=True)

    users = relationship("User", back_populates= "fonctions")
    rubriques = relationship("Rubrique", back_populates= "fonctions")
    

    def __init__(self, nature, description, *args, **kwargs):
        self.nature = nature
        self.description = description
        


class User(TimesCreate, TimesUpdate, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique= True, index =True)
    email = Column(String(50), nullable=False, unique= True, index = True)
    im = Column(Integer, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    fonction_id = Column(Integer, ForeignKey("fonctions.id"), nullable=True)
    fonctions = relationship("Fonction", back_populates= "users")


    fonctions = relationship("Fonction", back_populates= "users")
    rubriques = relationship("Rubrique", back_populates= "users")
    ogts = relationship("Ogt", back_populates= "users")
    versionogts = relationship("VersionOgt", back_populates= "users")
    saisis = relationship("Saisi", back_populates= "users")
    suivisaisis = relationship("SuiviSaisi", back_populates= "users")
    suivivalidations = relationship("SuiviValidation", back_populates= "users")

    
    def __init__(self, username, email, im, hashed_password, is_active, is_superuser, *args, **kwargs):
        self.username = username
        self.email = email
        self.im = im
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_superuser = is_superuser
       


class Ogt(TimesCreate, TimesUpdate, Base):
    __tablename__ = "ogts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intitule = Column(String(50), nullable=False, unique= True)
    abrev = Column(String(50), nullable=True, unique= True)
    niveau = Column(Integer, nullable=True)
    description = Column(String(50), nullable=True)

    userc_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("User", back_populates= "ogts")

    rubriques = relationship("Rubrique", back_populates= "ogts")

    def __init__(
        self, intitule, abrev, niveau, description, userc_id,
        *args, **kwargs
        ):
        self.intitule = intitule
        self.abrev = abrev
        self.niveau = niveau
        self.description = description
        self.userc_id = userc_id

class Rubrique(TimesCreate, TimesUpdate, Base):
    __tablename__ = "rubriques"
    id = Column(Integer, primary_key=True, autoincrement=True)
    intitule = Column(String(50), nullable=False, unique= True)
    abrev = Column(String(50), nullable=True, unique= True)
    niveau_saisi = Column(Integer, nullable=True)
    niveau_sorti = Column(Integer, nullable=True)
    description = Column(String(50), nullable=True)

    fonction_id = Column(Integer, ForeignKey("fonctions.id"), nullable=False)
    fonctions = relationship("Fonction", back_populates= "rubriques")
    ogt_id = Column(Integer, ForeignKey("ogts.id"), nullable=False)
    ogts = relationship("Ogt", back_populates= "rubriques")
    userc_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("User", back_populates= "rubriques")

    saisis = relationship("Saisi", back_populates= "rubriques")

    def __init__(
        self, intitule, abrev, niveau_saisi, niveau_sorti, description,ogt_id,
        fonction_id, userc_id,  *args, **kwargs
        ):
        self.intitule = intitule
        self.abrev = abrev
        self.niveau_saisi = niveau_saisi
        self.niveau_sorti = niveau_sorti
        self.description = description
        self.fonction_id = fonction_id
        self.userc_id = userc_id
        self.ogt_id=ogt_id



class VersionOgt(TimesCreate, TimesUpdate, Base):
    __tablename__ = "versionogts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    annee = Column(Integer, nullable=False)
    periode = Column(Integer, nullable=False)
    typeogt = Column(String(50), nullable=False)
    version = Column(String(50), nullable=False)
    description = Column(String(50), nullable=True)
    
    userc_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("User", back_populates= "versionogts")

    saisis = relationship("Saisi", back_populates= "versionogts")

    def __init__(self, annee, periode, typeogt, version, description, userc_id, *args, **kwargs):
        self.annee = annee
        self.periode = periode
        self.typeogt = typeogt
        self.version = version
        self.description = description
        self.userc_id = userc_id

class Saisi(TimesCreate, Base):
    __tablename__ = "saisis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    montant = Column(Float, nullable=True)
    description = Column(String(50), nullable=False)

    rubrique_id = Column(Integer, ForeignKey("rubriques.id"), nullable=False)
    rubriques = relationship("Rubrique", back_populates= "saisis")
    versionogt_id = Column(Integer, ForeignKey("versionogts.id"), nullable=False)
    versionogts = relationship("VersionOgt", back_populates= "saisis")
    userc_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("User", back_populates= "saisis")

    suivisaisis = relationship("SuiviSaisi", back_populates= "saisis")
    validations = relationship("Validation", back_populates= "saisis")
    
    def __init__(self, montant, description, rubrique_id, versionogt_id, userc_id, *args, **kwargs):
        self.montant = montant
        self.description = description
        self.rubrique_id = rubrique_id
        self.versionogt_id = versionogt_id
        self.userc_id = userc_id


class SuiviSaisi(TimesUpdate, Base):
    __tablename__ = "suivisaisis"
    id = Column(Integer, primary_key=True, autoincrement=True)

    saisi_id = Column(Integer, ForeignKey("saisis.id"), nullable=False)
    saisis = relationship("Saisi", back_populates= "suivisaisis")
    userc_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("User", back_populates= "suivisaisis")

    def __init__(self, saisi_id, userc_id, *args, **kwargs):
        self.saisi_id = saisi_id
        self.userc_id = userc_id


class Validation(TimesCreate, Base):
    __tablename__ = "validations"
    id = Column(Integer, primary_key=True, autoincrement=True)

    is_valide = Column(Boolean, default=False)

    saisi_id = Column(Integer, ForeignKey("saisis.id"), nullable=False)
    saisis = relationship("Saisi", back_populates= "validations")

    suivivalidations = relationship("SuiviValidation", back_populates= "validations")

    def __init__(self, is_valide, saisi_id, *args, **kwargs):
        self.is_valide = is_valide
        self.saisi_id = saisi_id
        
    
class SuiviValidation(TimesCreate, TimesUpdate, Base):
    __tablename__ = "suivivalidations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(30), nullable=False)


    validation_id = Column(Integer, ForeignKey("validations.id"), nullable=False)
    validations = relationship("Validation", back_populates= "suivivalidations")

    userc_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("User", back_populates= "suivivalidations")
    
    def __init__(self, action, validation_id, userc_id, *args, **kwargs):
        self.action = action
        self.validation_id = validation_id
        self.userc_id = userc_id

