from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class UserRegistrationSchema(Schema):
    """Schéma de validation pour l'inscription d'un utilisateur"""
    email = fields.Email(required=True, error_messages={
        "required": "L'email est requis",
        "invalid": "Format d'email invalide"
    })
    password = fields.Str(required=True, validate=validate.Length(min=6), error_messages={
        "required": "Le mot de passe est requis",
        "invalid": "Le mot de passe doit contenir au moins 6 caractères"
    })
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Le prénom est requis"
    })
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Le nom est requis"
    })
    phone = fields.Str(required=False, validate=validate.Length(max=20))
    birth_date = fields.Date(required=False)
    address = fields.Nested(lambda: AddressSchema(), required=False)
    bio = fields.Str(required=False, validate=validate.Length(max=500))
    profile_picture = fields.Str(required=False)

class AddressSchema(Schema):
    """Schéma pour l'adresse"""
    street = fields.Str(required=False)
    city = fields.Str(required=False)
    postal_code = fields.Str(required=False)
    country = fields.Str(required=False)

class UserLoginSchema(Schema):
    """Schéma de validation pour la connexion"""
    email = fields.Email(required=True, error_messages={
        "required": "L'email est requis",
        "invalid": "Format d'email invalide"
    })
    password = fields.Str(required=True, error_messages={
        "required": "Le mot de passe est requis"
    })

class UserUpdateSchema(Schema):
    """Schéma de validation pour la mise à jour d'un utilisateur"""
    first_name = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    phone = fields.Str(required=False, validate=validate.Length(max=20))
    birth_date = fields.Date(required=False)
    address = fields.Nested(AddressSchema, required=False)
    bio = fields.Str(required=False, validate=validate.Length(max=500))
    profile_picture = fields.Str(required=False)

def validate_user_registration(data):
    """Valide les données d'inscription"""
    schema = UserRegistrationSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_user_login(data):
    """Valide les données de connexion"""
    schema = UserLoginSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_user_update(data):
    """Valide les données de mise à jour"""
    schema = UserUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None