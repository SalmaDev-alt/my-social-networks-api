from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import datetime

class EventCreateSchema(Schema):
    """Schéma de validation pour la création d'un événement"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required": "Le nom de l'événement est requis"
    })
    description = fields.Str(required=True, validate=validate.Length(min=1, max=2000), error_messages={
        "required": "La description est requise"
    })
    start_date = fields.DateTime(required=True, error_messages={
        "required": "La date de début est requise"
    })
    end_date = fields.DateTime(required=True, error_messages={
        "required": "La date de fin est requise"
    })
    location = fields.Str(required=True, validate=validate.Length(min=1, max=300), error_messages={
        "required": "Le lieu est requis"
    })
    cover_photo = fields.Str(required=False)
    is_private = fields.Bool(required=False, missing=False)
    organizers = fields.List(fields.Str(), required=False)
    participants = fields.List(fields.Str(), required=False)
    group_id = fields.Str(required=False)
    has_ticketing = fields.Bool(required=False, missing=False)
    has_shopping_list = fields.Bool(required=False, missing=False)
    has_carpooling = fields.Bool(required=False, missing=False)
    
    @validates_schema
    def validate_dates(self, data, **kwargs):
        """Vérifie que la date de fin est après la date de début"""
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] <= data['start_date']:
                raise ValidationError("La date de fin doit être après la date de début")

class EventUpdateSchema(Schema):
    """Schéma de validation pour la mise à jour d'un événement"""
    name = fields.Str(required=False, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=False, validate=validate.Length(min=1, max=2000))
    start_date = fields.DateTime(required=False)
    end_date = fields.DateTime(required=False)
    location = fields.Str(required=False, validate=validate.Length(min=1, max=300))
    cover_photo = fields.Str(required=False)
    is_private = fields.Bool(required=False)
    has_shopping_list = fields.Bool(required=False)
    has_carpooling = fields.Bool(required=False)
    
    @validates_schema
    def validate_dates(self, data, **kwargs):
        """Vérifie que la date de fin est après la date de début"""
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] <= data['start_date']:
                raise ValidationError("La date de fin doit être après la date de début")

def validate_event_create(data):
    """Valide les données de création d'événement"""
    schema = EventCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_event_update(data):
    """Valide les données de mise à jour d'événement"""
    schema = EventUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None