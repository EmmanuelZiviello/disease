from F_taste_disease.ma import ma
from F_taste_disease.models.intolleranza import IntolleranzaModel
from marshmallow import fields

class IntolleranzaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IntolleranzaModel
        load_instance = True
    id_paziente = fields.String(required=False)