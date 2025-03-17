from F_taste_disease.db import Base
from sqlalchemy import Column, Integer, String
class PatologiaModel(Base):
    __tablename__ = "patologia"
    id_patologia = Column(Integer, primary_key=True)
    patologia = Column(String(600), unique=True, nullable=False)
    id_paziente = Column(String(7), nullable=False, unique=True) 

    def __init__(self, patologia,id_paziente):
        self.patologia = patologia
        self.id_paziente=id_paziente

    def __repr__(self):
        return "PatologiaModel(patologia:%s)" % (self.patologia)

    def __json__(self):
        return { 'name': self.patologia }