from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class TicketTypeCreateSchema(Schema):
    """Schéma de validation pour la création d'un type de billet"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required": "Le nom du type de billet est requis"
    })
    price = fields.Float(required=True, validate=validate.Range(min=0), error_messages={
        "required": "Le prix est requis"
    })
    quantity = fields.Int(required=True, validate=validate.Range(min=1), error_messages={
        "required": "La quantité est requise"
    })
    description = fields.Str(required=False, validate=validate.Length(max=500))

class TicketPurchaseSchema(Schema):
    """Schéma de validation pour l'achat d'un billet"""
    ticket_type_id = fields.Str(required=True, error_messages={
        "required": "L'ID du type de billet est requis"
    })
    buyer_first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Le prénom de l'acheteur est requis"
    })
    buyer_last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Le nom de l'acheteur est requis"
    })
    buyer_email = fields.Email(required=True, error_messages={
        "required": "L'email de l'acheteur est requis",
        "invalid": "Format d'email invalide"
    })
    buyer_address = fields.Nested(lambda: BuyerAddressSchema(), required=True, error_messages={
        "required": "L'adresse de l'acheteur est requise"
    })

class BuyerAddressSchema(Schema):
    """Schéma pour l'adresse complète de l'acheteur"""
    street = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required": "La rue est requise"
    })
    city = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "La ville est requise"
    })
    postal_code = fields.Str(required=True, validate=validate.Length(min=1, max=20), error_messages={
        "required": "Le code postal est requis"
    })
    country = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Le pays est requis"
    })

def validate_ticket_type_create(data):
    """Valide les données de création de type de billet"""
    schema = TicketTypeCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_ticket_purchase(data):
    """Valide les données d'achat de billet"""
    schema = TicketPurchaseSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None