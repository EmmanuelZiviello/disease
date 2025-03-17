from F_taste_disease.db import Base
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class AllergiaModel(Base):
    __tablename__ = "allergia"
    id_allergia = Column(Integer, primary_key=True)
    allergia = Column(String(600), nullable=False)
    id_paziente = Column(String(7), nullable=True)  
    #stessa condizione presente più volte nel db ma con id paziente diverso
    #es nome="Diabete di tipo II" associato a 2 pazienti con id diverso
    __table_args__ = (
        UniqueConstraint(id_paziente, allergia, name="allergy_patient"),
    )

    def __repr__(self):
        return "AllergiaModel(allergia:%s)" % (self.allergia)

    def __json__(self):
        return { 'name': self.allergia}

    def __init__(self, allergia):
        self.allergia = allergia