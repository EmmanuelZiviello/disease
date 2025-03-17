from F_taste_disease.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import StringEncryptedType

class IntolleranzaModel(Base):
    __tablename__ = "intolleranza"
    id_intolleranza = Column(Integer, primary_key=True)
    intolleranza =  Column(String(600), nullable=False)
    id_paziente = Column(String(7), nullable=True)
    #stessa condizione presente più volte nel db ma con id paziente diverso
    #es nome="Diabete di tipo II" associato a 2 pazienti con id diverso
    __table_args__ = (
        UniqueConstraint(id_paziente, intolleranza, name="intollerance_patient"),
    )  

    def __repr__(self):
        return "IntolleranzaModel(intolleranza:%s)" % (self.intolleranza)

    def __json__(self):
        return { 'name': self.intolleranza}

    def __init__(self, intolleranza):
        self.intolleranza = intolleranza