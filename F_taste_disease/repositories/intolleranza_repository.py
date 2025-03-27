from F_taste_disease.db import get_session
from F_taste_disease.models.intolleranza import IntolleranzaModel



class IntolleranzaRepository:

    @staticmethod
    def get_all_intolleranze(session=None):
        session = session or get_session('dietitian')
        try:
            # Eseguiamo la query per ottenere tutte le intolleranze
            intolleranze = session.query(IntolleranzaModel).all()
            # Aggiungiamo il nome di ogni intolleranza alla lista result
            return [intolleranza.intolleranza for intolleranza in intolleranze]
        except Exception:
            # In caso di errore, ritorniamo una lista vuota
            return []
        
    @staticmethod
    def find_by_id_paziente(id_paziente, session=None):
        session = session or get_session('dietitian')
        try:
            # Eseguiamo la query per ottenere tutte le intolleranze per un determinato id_paziente
            intolleranze = session.query(IntolleranzaModel).filter_by(id_paziente=id_paziente).all()
            # Restituiamo un elenco di intolleranze per il paziente specificato
            return [intolleranza.intolleranza for intolleranza in intolleranze]
        except Exception as e:
            # In caso di errore, ritorniamo una lista vuota
            return []
        
    @staticmethod
    def add(intolleranza, session=None):
        session=session or get_session('dietitian')
        session.add(intolleranza)
        session.commit()  