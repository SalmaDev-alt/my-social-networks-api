from marshmallow import Schema, fields, validate

class AlbumCreateSchema(Schema):
    """Schéma de validation pour la création d'un album"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required": "Le nom de l'album est requis"
    })
    description = fields.Str(required=False, validate=validate.Length(max=1000))
    event_id = fields.Str(required=True, error_messages={
        "required": "L'ID de l'événement est requis"
    })

class PhotoCreateSchema(Schema):
    """Schéma de validation pour l'ajout d'une photo"""
    url = fields.Str(required=True, error_messages={
        "required": "L'URL de la photo est requise"
    })
    caption = fields.Str(required=False, validate=validate.Length(max=500))
    album_id = fields.Str(required=True, error_messages={
        "required": "L'ID de l'album est requis"
    })

class CommentCreateSchema(Schema):
    """Schéma de validation pour un commentaire sur une photo"""
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000), error_messages={
        "required": "Le contenu du commentaire est requis"
    })

def validate_album_create(data):
    """Valide les données de création d'album"""
    schema = AlbumCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_photo_create(data):
    """Valide les données d'ajout de photo"""
    schema = PhotoCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_comment_create(data):
    """Valide les données de création de commentaire"""
    schema = CommentCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None