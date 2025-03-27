from F_taste_disease.db import get_session
from F_taste_disease.models.allergia import AllergiaModel



class AllergiaRepository:

    @staticmethod
    def get_all_allergie(session=None):
        session = session or get_session('dietitian')
        try:
            # Eseguiamo la query per ottenere tutte le allergie
            allergie = session.query(AllergiaModel).all()
            # Aggiungiamo il nome di ogni allergia alla lista result
            return [allergia.allergia for allergia in allergie]
        except Exception:
            # In caso di errore, ritorniamo una lista vuota
            return []
        
    @staticmethod
    def find_by_id_paziente(id_paziente, session=None):
        session = session or get_session('dietitian')
        try:
            # Eseguiamo la query per ottenere tutte le allergie per un determinato id_paziente
            allergie = session.query(AllergiaModel).filter_by(id_paziente=id_paziente).all()
            # Restituiamo un elenco di allergie per il paziente specificato
            return [allergia.allergia for allergia in allergie]
        except Exception as e:
            # In caso di errore, ritorniamo una lista vuota
            return []
        
    @staticmethod
    def add(allergia, session=None):
        session=session or get_session('dietitian')
        session.add(allergia)
        session.commit()  