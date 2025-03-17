from F_taste_disease.ma import ma
from F_taste_disease.models.allergia import AllergiaModel
from marshmallow import fields

class AllergiaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllergiaModel
        load_instance = True
    id_paziente = fields.String(required=False)