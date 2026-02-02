from marshmallow import Schema, fields, validate

class CarpoolingCreateSchema(Schema):
    """Schéma de validation pour la création d'une offre de covoiturage"""
    departure_location = fields.Str(required=True, validate=validate.Length(min=1, max=300), error_messages={
        "required": "Le lieu de départ est requis"
    })
    departure_time = fields.DateTime(required=True, error_messages={
        "required": "L'heure de départ est requise"
    })
    price = fields.Float(required=True, validate=validate.Range(min=0), error_messages={
        "required": "Le prix est requis"
    })
    available_seats = fields.Int(required=True, validate=validate.Range(min=1, max=8), error_messages={
        "required": "Le nombre de places disponibles est requis"
    })
    max_time_difference = fields.Int(required=True, validate=validate.Range(min=0), error_messages={
        "required": "Le temps d'écart maximum est requis (en minutes)"
    })
    event_id = fields.Str(required=True, error_messages={
        "required": "L'ID de l'événement est requis"
    })
    notes = fields.Str(required=False, validate=validate.Length(max=500))

class CarpoolingUpdateSchema(Schema):
    """Schéma de validation pour la mise à jour d'une offre"""
    price = fields.Float(required=False, validate=validate.Range(min=0))
    available_seats = fields.Int(required=False, validate=validate.Range(min=0, max=8))
    notes = fields.Str(required=False, validate=validate.Length(max=500))

class CarpoolingBookingSchema(Schema):
    """Schéma de validation pour la réservation d'une place"""
    seats_requested = fields.Int(required=True, validate=validate.Range(min=1), error_messages={
        "required": "Le nombre de places demandées est requis"
    })

def validate_carpooling_create(data):
    """Valide les données de création d'offre de covoiturage"""
    schema = CarpoolingCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_carpooling_update(data):
    """Valide les données de mise à jour d'offre"""
    schema = CarpoolingUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_carpooling_booking(data):
    """Valide les données de réservation"""
    schema = CarpoolingBookingSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None