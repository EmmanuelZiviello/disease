from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import get_jwt_identity
from F_taste_disease.namespaces import nutrizionista_ns
from F_taste_disease.utils.jwt_custom_decorators import nutrizionista_required
from F_taste_disease.services.disease_service import DiseaseService

disease_request_model = nutrizionista_ns.model('disease', {
    "disease": fields.String(description="Patologia del paziente", example="Diabete tipo II", required=True),
    "id_paziente": fields.String(description="ID paziente", example="PAZ1234", required=True)
}, strict=True)



class Disease(Resource):

    #da provare(problema che le condizioni devono essere già nel db)
    @nutrizionista_required()
    @nutrizionista_ns.expect(disease_request_model)
    @nutrizionista_ns.doc('Inserisci una condizione al paziente')
    def post(self):
        request_json=request.get_json()
        email_nutrizionista = get_jwt_identity()
        return DiseaseService.add_disease_to_patient(request_json["id_paziente"],request_json["disease"],email_nutrizionista)
    
    #da provare(problema che le condizioni devono essere già nel db)
    @nutrizionista_required()
    @nutrizionista_ns.doc('Elimina una patologia al paziente', params={'fk_paziente': 'PAZ1234', 'patologia': 'una_patologia'})
    def delete(self):
        request_data = request.args
        validation_errors = disease_request_model.validate(request_data)
        if validation_errors:
            return validation_errors, 400
        
        email_nutrizionista=get_jwt_identity()

        return DiseaseService.delete_disease(
            email_nutrizionista,
            id_paziente=request_data['id_paziente'],
            disease=request_data['disease']
        )
    
class AllDisease(Resource):

    #da provare
    @nutrizionista_required()
    @nutrizionista_ns.doc('Ottieni tutte le patologie')
    def get(self):
        

        try:
            # Usiamo il service per ottenere i dati elaborati
            data = DiseaseService.process_data()

            # Se i dati sono validi, restituiamo la risposta con codice 200
            if data:
                return data, 200

            # Altrimenti restituiamo una lista vuota
            return [], 200

        except Exception:
            return {"message": "Internal Server Error"}, 500
        
class DiseaseDelPaziente(Resource):

    #da provare
    @nutrizionista_required()
    @nutrizionista_ns.doc("ricevi le condizioni associate ad un paziente", params={'id_paziente': 'PAZ1234'})
    def get(self):
        request_args = request.args
        email_nutrizionista = get_jwt_identity()

        if "id_paziente" not in request_args:
            return {"error": "Il campo id_paziente è obbligatorio."}, 400


        return DiseaseService.get_conditions(request_args["id_paziente"], email_nutrizionista)
