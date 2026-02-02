from marshmallow import Schema, fields, validate

class GroupCreateSchema(Schema):
    """Schéma de validation pour la création d'un groupe"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required": "Le nom du groupe est requis"
    })
    description = fields.Str(required=True, validate=validate.Length(min=1, max=2000), error_messages={
        "required": "La description est requise"
    })
    icon = fields.Str(required=False)
    cover_photo = fields.Str(required=False)
    group_type = fields.Str(
        required=True, 
        validate=validate.OneOf(['public', 'private', 'secret']),
        error_messages={
            "required": "Le type de groupe est requis",
            "invalid": "Le type doit être: public, private ou secret"
        }
    )
    allow_members_to_post = fields.Bool(required=False, missing=True)
    allow_members_to_create_events = fields.Bool(required=False, missing=True)
    members = fields.List(fields.Str(), required=False)

class GroupUpdateSchema(Schema):
    """Schéma de validation pour la mise à jour d'un groupe"""
    name = fields.Str(required=False, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=False, validate=validate.Length(min=1, max=2000))
    icon = fields.Str(required=False)
    cover_photo = fields.Str(required=False)
    group_type = fields.Str(required=False, validate=validate.OneOf(['public', 'private', 'secret']))
    allow_members_to_post = fields.Bool(required=False)
    allow_members_to_create_events = fields.Bool(required=False)

def validate_group_create(data):
    """Valide les données de création de groupe"""
    schema = GroupCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_group_update(data):
    """Valide les données de mise à jour de groupe"""
    schema = GroupUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None