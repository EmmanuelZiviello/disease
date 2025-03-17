from F_taste_disease.db import get_session
from F_taste_disease.repositories.patologia_repository import PatologiaRepository
from F_taste_disease.repositories.intolleranza_repository import IntolleranzaRepository
from F_taste_disease.repositories.allergia_repository import AllergiaRepository
from F_taste_disease.repositories.disease_repository import DiseaseRepository
from F_taste_disease.kafka.kafka_producer import send_kafka_message
from F_taste_disease.utils.kafka_helpers import wait_for_kafka_response


class DiseaseService:



    @staticmethod
    def add_disease_to_patient(id_paziente,disease,email_nutrizionista):
      #invia tramite kafka per capire se è presente il paziente nel db e riceve status e id_nutrizionista
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.existGet.request",message)
        response_paziente=wait_for_kafka_response(["patient.existGet.success", "patient.existGet.failed"])
        #controlli su response_paziente
        if response_paziente is None:
            return {"message": "Errore nella comunicazione con Kafka"}, 500
        
        if response_paziente.get("status_code") == "200":
            paziente_id_nutrizionista=response_paziente["id_nutrizionista"]
            if paziente_id_nutrizionista:
                #invia tramite kafka per capire se è presente il nutrizionista nel db e riceve il suo id
                message={"email_nutrizionista":email_nutrizionista}
                send_kafka_message("dietitian.existGet.request",message)
                response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
                #controlli su response_nutrizionista
                if response_nutrizionista is None:
                    return {"message": "Errore nella comunicazione con Kafka"}, 500
                
                if response_nutrizionista.get("status_code") == "200":
                    id_nutrizionista=response_nutrizionista["id_nutrizionista"]

                    if id_nutrizionista:
                    #   
                        if paziente_id_nutrizionista == id_nutrizionista:
                                session = get_session('dietitian')
                                if not DiseaseRepository.check_association(disease,id_paziente, session):
                                    DiseaseRepository.associate_disease(id_paziente,disease,session)
                                    session.close()
                                    return {"message:""Condizione associata con successo"}, 200 
                                else:
                                    session.close()
                                    return {'message': 'il paziente  è già associato alla condizione'}, 404
                        else:
                            return {'message': 'paziente non seguito'}, 403
                        
                    else:
                        return{"message":"Id nutrizionista mancante"}, 400
                    #
                elif response_nutrizionista.get("status_code") == "400":
                    return {"esito add_disease_to_patient":"Dati mancanti"}, 400
                elif response_nutrizionista.get("status_code") == "404":
                    return {"esito add_disease_to_patient":"Nutrizionista non presente nel db"}, 404
            
            return{"message":"Il paziente non è seguito da un nutrizionista"}, 403

            
        elif response_paziente.get("status_code") == "400":
            return {"esito add_disease_to_patient":"Dati mancanti"}, 400
        elif response_paziente.get("status_code") == "404":
            return {"esito add_disease_to_patient":"Paziente non presente nel db"}, 404
        

    @staticmethod
    def delete_disease(email_nutrizionista,id_paziente,disease):
         #invia tramite kafka per capire se è presente il paziente nel db e riceve status e id_nutrizionista
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.existGet.request",message)
        response_paziente=wait_for_kafka_response(["patient.existGet.success", "patient.existGet.failed"])
        #controlli su response_paziente
        if response_paziente is None:
            return {"message": "Errore nella comunicazione con Kafka"}, 500
        
        if response_paziente.get("status_code") == "200":
            paziente_id_nutrizionista=response_paziente["id_nutrizionista"]
            if paziente_id_nutrizionista:
                #invia tramite kafka per capire se è presente il nutrizionista nel db e riceve il suo id
                message={"email_nutrizionista":email_nutrizionista}
                send_kafka_message("dietitian.existGet.request",message)
                response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
                #controlli su response_nutrizionista
                if response_nutrizionista is None:
                    return {"message": "Errore nella comunicazione con Kafka"}, 500
                
                if response_nutrizionista.get("status_code") == "200":
                    id_nutrizionista=response_nutrizionista["id_nutrizionista"]

                    if id_nutrizionista:
                    #   
                        if paziente_id_nutrizionista == id_nutrizionista:
                                session = get_session('dietitian')
                                if  DiseaseRepository.check_association(disease,id_paziente, session):
                                    DiseaseRepository.remove_disease_from_patient(id_paziente, disease, session)
                                    session.close()
                                    return {'message': 'Condizione disassociata con successo!'}, 200
                                else:
                                    session.close()
                                    return {'message': 'il paziente non soffre della condizione'}, 404
                        else:
                            return {'message': 'paziente non seguito'}, 403
                        
                    else:
                        return{"message":"Id nutrizionista mancante"}, 400
                    #
                elif response_nutrizionista.get("status_code") == "400":
                    return {"esito delete_disease":"Dati mancanti"}, 400
                elif response_nutrizionista.get("status_code") == "404":
                    return {"esito delete_disease":"Nutrizionista non presente nel db"}, 404
            
            return{"message":"Il paziente non è seguito da un nutrizionista"}, 403

            
        elif response_paziente.get("status_code") == "400":
            return {"esito delete_disease":"Dati mancanti"}, 400
        elif response_paziente.get("status_code") == "404":
            return {"esito delete_disease":"Paziente non presente nel db"}, 404
        





    @staticmethod
    def process_data():
        #Estrae i dati e verifica se sono validi prima di costruire la struttura finale
        try:
            # Estraiamo i dati
            patologie_names, allergie_names, intolleranze_names = DiseaseService.extract_data()

            # Se uno dei tre dataset è vuoto, restituiamo None
            if not (patologie_names and allergie_names and intolleranze_names):
                return None

            # Costruiamo la struttura finale
            return DiseaseService.construct_data_structure(patologie_names, allergie_names, intolleranze_names)

        except Exception:
            return None
        

    @staticmethod
    def extract_data():
        #Recupera i dati dal database e li restituisce come tuple
        session = get_session('dietitian')
        # Estraiamo i dati dalle repository
        patologie_names = PatologiaRepository.get_all_patologie(session)
        allergie_names = AllergiaRepository.get_all_allergie(session)
        intolleranze_names = IntolleranzaRepository.get_all_intolleranze(session)
        session.close()
        return patologie_names, allergie_names, intolleranze_names
        


    @staticmethod
    def construct_data_structure(pat_list, alg_list, int_list):
        #Costruisce la struttura JSON finale con i dati estratti
        return {
            "patologie": DiseaseService.create_components(pat_list),
            "allergie": DiseaseService.create_components(alg_list),
            "intolleranze": DiseaseService.create_components(int_list)
        }

    @staticmethod
    def create_components(items):
        #Converte una lista di stringhe in un elenco di dizionari con chiave 'name'
        return [{"name": item} for item in items]
    


    @staticmethod
    def get_conditions(id_paziente, email_nutrizionista):
        #invia tramite kafka per capire se è presente il paziente nel db e riceve status e id_nutrizionista
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.existGet.request",message)
        response_paziente=wait_for_kafka_response(["patient.existGet.success", "patient.existGet.failed"])
        #controlli su response_paziente
        if response_paziente is None:
            return {"message": "Errore nella comunicazione con Kafka"}, 500
        
        if response_paziente.get("status_code") == "200":
            paziente_id_nutrizionista=response_paziente["id_nutrizionista"]
            if paziente_id_nutrizionista:
                #invia tramite kafka per capire se è presente il nutrizionista nel db e riceve il suo id
                message={"email_nutrizionista":email_nutrizionista}
                send_kafka_message("dietitian.existGet.request",message)
                response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
                #controlli su response_nutrizionista
                if response_nutrizionista is None:
                    return {"message": "Errore nella comunicazione con Kafka"}, 500
                
                if response_nutrizionista.get("status_code") == "200":
                    id_nutrizionista=response_nutrizionista["id_nutrizionista"]

                    if id_nutrizionista:
                    #   
                        if paziente_id_nutrizionista == id_nutrizionista:
                                session = get_session('dietitian')
                                patologie=PatologiaRepository.find_by_id_paziente(id_paziente,session)
                                allergie=AllergiaRepository.find_by_id_paziente(id_paziente,session)
                                intolleranze=IntolleranzaRepository.find_by_id_paziente(id_paziente,session)
                                session.close()
                                return {
                                    "patologie":patologie,
                                    "allergie":allergie,
                                    "intolleranze":intolleranze
                                }, 200
                               
                        else:
                            return {'message': 'paziente non seguito'}, 403
                        
                    else:
                        return{"message":"Id nutrizionista mancante"}, 400
                    #
                elif response_nutrizionista.get("status_code") == "400":
                    return {"esito get_conditions":"Dati mancanti"}, 400
                elif response_nutrizionista.get("status_code") == "404":
                    return {"esito get_conditions":"Nutrizionista non presente nel db"}, 404
            
            return{"message":"Il paziente non è seguito da un nutrizionista"}, 403

            
        elif response_paziente.get("status_code") == "400":
            return {"esito get_conditions":"Dati mancanti"}, 400
        elif response_paziente.get("status_code") == "404":
            return {"esito get_conditions":"Paziente non presente nel db"}, 404