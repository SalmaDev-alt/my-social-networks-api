from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class PollQuestionSchema(Schema):
    """Schéma pour une question de sondage"""
    question = fields.Str(required=True, validate=validate.Length(min=1, max=500), error_messages={
        "required": "Le texte de la question est requis"
    })
    options = fields.List(
        fields.Str(validate=validate.Length(min=1, max=200)),
        required=True,
        validate=validate.Length(min=2),
        error_messages={
            "required": "Les options de réponse sont requises",
            "invalid": "Il faut au moins 2 options de réponse"
        }
    )

class PollCreateSchema(Schema):
    """Schéma de validation pour la création d'un sondage"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required": "Le titre du sondage est requis"
    })
    description = fields.Str(required=False, validate=validate.Length(max=1000))
    event_id = fields.Str(required=True, error_messages={
        "required": "L'ID de l'événement est requis"
    })
    questions = fields.List(
        fields.Nested(PollQuestionSchema),
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            "required": "Au moins une question est requise"
        }
    )
    allow_multiple_votes = fields.Bool(required=False, missing=False)

class PollResponseSchema(Schema):
    """Schéma de validation pour une réponse à un sondage"""
    responses = fields.List(
        fields.Dict(
            keys=fields.Str(),
            values=fields.Int()
        ),
        required=True,
        error_messages={
            "required": "Les réponses sont requises"
        }
    )
    # Format: [{"question_index": 0, "option_index": 1}, ...]

def validate_poll_create(data):
    """Valide les données de création de sondage"""
    schema = PollCreateSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None

def validate_poll_response(data):
    """Valide les données de réponse à un sondage"""
    schema = PollResponseSchema()
    errors = schema.validate(data)
    if errors:
        return False, errors
    return True, None