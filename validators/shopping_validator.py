from marshmallow import Schema, fields, validate

class ShoppingItemCreateSchema(Schema):
    """Schéma de validation pour la création d'un item de shopping list"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required": "Le nom de l'item est requis"
    })
    quantity = fields.Int(required=True, validate=validate.Range(min=1), error_messages={
        "required": "La quantité est requise"
    })
    arrival_time = fields.DateTime(required=True, error_messages={
        "required": "L'heure d'arrivée est requise"
    })
    event_id = fields.Str(required=True, error_messages={
        "required": "L'ID de l'événement est requis"
    })
    notes = fields.Str(required=False, validate=validate.Length(max=500))

class ShoppingItemUpdateSchema(Schema):
    """Schéma de validation pour la mise à jour d'un item"""
    quantity = fields.Int(required=False, validate=validate.Range(min=1))
    arrival_time = fields.DateTime(required=False)
    notes = fields.Str(required=False, validate=validate.Length(max=500))

def validate_shopping_item_create(data):
    """Valide les données de création d'item shopping"""
    schema = ShoppingItemCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_shopping_item_update(data):
    """Valide les données de mise à jour d'item shopping"""
    schema = ShoppingItemUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None