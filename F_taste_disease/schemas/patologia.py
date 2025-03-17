from F_taste_disease.ma import ma
from F_taste_disease.models.patologia import PatologiaModel
from marshmallow import fields

class PatologiaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatologiaModel
        load_instance = True
    id_paziente = fields.String(required=False)