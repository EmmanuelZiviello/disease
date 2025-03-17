from F_taste_disease.db import get_session
from F_taste_disease.models.patologia import PatologiaModel
from F_taste_disease.models.allergia import AllergiaModel
from F_taste_disease.models.intolleranza import IntolleranzaModel


class DiseaseRepository:

    @staticmethod
    def check_association(disease, id_paziente, session=None):
        session = session or get_session('dietitian')

        return (
            session.query(PatologiaModel).filter_by(id_paziente=id_paziente, patologia=disease).first() is not None or
            session.query(AllergiaModel).filter_by(id_paziente=id_paziente, allergia=disease).first() is not None or
            session.query(IntolleranzaModel).filter_by(id_paziente=id_paziente, intolleranza=disease).first() is not None
        )

    @staticmethod
    def associate_disease(id_paziente, disease, session=None):
        session = session or get_session('dietitian')

        disease_model = DiseaseRepository.find_disease_model(disease, session)
        if not disease_model:
            raise ValueError(f"Condizione non trovata: {disease}")

        # Creiamo un nuovo record con l'id_paziente
        if isinstance(disease_model, PatologiaModel):
            new_disease = PatologiaModel(patologia=disease, id_paziente=id_paziente)
        elif isinstance(disease_model, AllergiaModel):
            new_disease = AllergiaModel(allergia=disease, id_paziente=id_paziente)
        elif isinstance(disease_model, IntolleranzaModel):
            new_disease = IntolleranzaModel(intolleranza=disease, id_paziente=id_paziente)
        else:
            raise ValueError("Tipo di condizione non riconosciuto")

        session.add(new_disease)
        session.commit()

    @staticmethod
    def find_disease_model(disease, session=None):
        session = session or get_session('dietitian')
        return (
            session.query(PatologiaModel).filter_by(patologia=disease).first() or
            session.query(AllergiaModel).filter_by(allergia=disease).first() or
            session.query(IntolleranzaModel).filter_by(intolleranza=disease).first()
        )


    @staticmethod
    def remove_disease_from_patient(id_paziente, disease, session=None):
        session = session or get_session('dietitian')

        disease_model = (
            session.query(PatologiaModel).filter_by(id_paziente=id_paziente, patologia=disease).first() or
            session.query(AllergiaModel).filter_by(id_paziente=id_paziente, allergia=disease).first() or
            session.query(IntolleranzaModel).filter_by(id_paziente=id_paziente, intolleranza=disease).first()
        )

        if not disease_model:
            raise ValueError(f"Condizione {disease} non trovata per il paziente {id_paziente}")

        session.delete(disease_model)
        session.commit()
                

    
