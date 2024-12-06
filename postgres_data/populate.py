import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, String, DateTime, Float, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database

engine= create_engine('postgresql://admin:password@postgres_container:5432/france_travail_clean')

if not database_exists(engine.url):
    create_database(engine.url)

df = pd.read_csv("data/france_travail_clean.csv")

print(df.shape)
print(df.head())
print(df.columns)

Base = declarative_base()

class JobOffer(Base):
    __tablename__ = "france_travail"
    id = Column(String, primary_key=True)
    intitule = Column(String)
    description = Column(Text)
    dateCreation = Column(DateTime)
    dateActualisation = Column(DateTime)
    lieuTravail_latitude = Column(Float)
    lieuTravail_longitude = Column(Float)
    lieuTravail_libelle = Column(String)
    romeCode = Column(String)
    typeContrat = Column(String)
    experienceExige = Column(String)
    alternance = Column(String)
    origineOffre_urlOrigine = Column(String)
    dureeTravailLibelleConverti = Column(String)
    competences = Column(String)
    qualitesProfessionnelles = Column(String)
    formations = Column(String)

Base.metadata.create_all(engine)

df.to_sql("france_travail", engine, if_exists="replace", index=False)