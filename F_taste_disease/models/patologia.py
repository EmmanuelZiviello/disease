from F_taste_disease.db import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint
class PatologiaModel(Base):
    __tablename__ = "patologia"
    id_patologia = Column(Integer, primary_key=True)
    patologia = Column(String(600), nullable=False)
    id_paziente = Column(String(7), nullable=True)
    #stessa condizione presente più volte nel db ma con id paziente diverso
    #es nome="Diabete di tipo II" associato a 2 pazienti con id diverso
    __table_args__ = (
        UniqueConstraint(id_paziente, patologia, name="patology_patient"),
    ) 

    def __init__(self, patologia):
        self.patologia = patologia
        

    def __repr__(self):
        return "PatologiaModel(patologia:%s)" % (self.patologia)

    def __json__(self):
        return { 'name': self.patologia }