import os


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



DATABASE_URL = os.environ.get("DATABASE_URL")

#initialisé le moteur sqlalchemy (echo=False en mode de production)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#création d'une session sqlalchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# A retirer si alembic
"""
def init_db():
    Base.metadata.create_all(engine)
"""



