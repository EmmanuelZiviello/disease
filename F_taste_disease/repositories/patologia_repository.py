from F_taste_disease.db import get_session
from F_taste_disease.models.patologia import PatologiaModel



class PatologiaRepository:

    @staticmethod
    def get_all_patologie(session=None):
        session = session or get_session('dietitian')
        try:
            # Eseguiamo la query per ottenere tutte le patologie
            patologie = session.query(PatologiaModel).all()
            # Aggiungiamo il nome di ogni patologia alla lista result
            return [patologia.patologia for patologia in patologie]
        except Exception:
            # In caso di errore, ritorniamo una lista vuota
            return []
        
    @staticmethod
    def find_by_id_paziente(id_paziente, session=None):
        session = session or get_session('dietitian')
        try:
            # Eseguiamo la query per ottenere tutte le patologie per un determinato id_paziente
            patologie = session.query(PatologiaModel).filter_by(id_paziente=id_paziente).all()
            # Restituiamo un elenco di patologie per il paziente specificato
            return [patologia.patologia for patologia in patologie]
        except Exception as e:
            # In caso di errore, ritorniamo una lista vuota
            return []
        
    @staticmethod
    def add(patologia, session=None):
        session=session or get_session('dietitian')
        session.add(patologia)
        session.commit()  