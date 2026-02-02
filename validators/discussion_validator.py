from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class MessageCreateSchema(Schema):
    """Schéma de validation pour la création d'un message"""
    content = fields.Str(required=True, validate=validate.Length(min=1, max=5000), error_messages={
        "required": "Le contenu du message est requis"
    })
    parent_message_id = fields.Str(required=False)

class DiscussionCreateSchema(Schema):
    """Schéma de validation pour la création d'une discussion"""
    event_id = fields.Str(required=False)
    group_id = fields.Str(required=False)
    
    @validates_schema
    def validate_reference(self, data, **kwargs):
        """Vérifie qu'une discussion est liée soit à un événement soit à un groupe"""
        event_id = data.get('event_id')
        group_id = data.get('group_id')
        
        if not event_id and not group_id:
            raise ValidationError("Une discussion doit être liée à un événement ou un groupe")
        
        if event_id and group_id:
            raise ValidationError("Une discussion ne peut pas être liée à la fois à un événement et un groupe")

def validate_message_create(data):
    """Valide les données de création de message"""
    schema = MessageCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_discussion_create(data):
    """Valide les données de création de discussion"""
    schema = DiscussionCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None