from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required
from validators import validate_poll_create, validate_poll_response

polls_bp = Blueprint('polls', __name__, url_prefix='/api/polls')

@polls_bp.route('', methods=['POST'])
@token_required
def create_poll(current_user):
    """Créer un sondage"""
    try:
        data = request.get_json()
        is_valid, errors = validate_poll_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(data['event_id'])})
        if not event or ObjectId(current_user['_id']) not in event['organizers']:
            return error_response("Seuls les organisateurs peuvent créer des sondages", 403)
        
        poll_data = {
            "title": data['title'],
            "description": data.get('description'),
            "event_id": ObjectId(data['event_id']),
            "questions": data['questions'],
            "allow_multiple_votes": data.get('allow_multiple_votes', False),
            "responses": [],
            "created_by": ObjectId(current_user['_id']),
            "created_at": datetime.utcnow()
        }
        
        result = db.polls.insert_one(poll_data)
        poll = db.polls.find_one({"_id": result.inserted_id})
        
        return created_response(poll, "Sondage créé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@polls_bp.route('/event/<event_id>', methods=['GET'])
@token_required
def get_event_polls(current_user, event_id):
    """Récupérer les sondages d'un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        polls = list(db.polls.find({"event_id": ObjectId(event_id)}))
        return success_response({"polls": polls})
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@polls_bp.route('/<poll_id>', methods=['GET'])
@token_required
def get_poll(current_user, poll_id):
    """Récupérer un sondage par son ID"""
    try:
        if not ObjectId.is_valid(poll_id):
            return error_response("ID sondage invalide", 400)
        
        db = get_db()
        poll = db.polls.find_one({"_id": ObjectId(poll_id)})
        if not poll:
            return not_found_response("Sondage non trouvé")
        
        event = db.events.find_one({"_id": poll['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        return success_response(poll)
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@polls_bp.route('/<poll_id>', methods=['DELETE'])
@token_required
def delete_poll(current_user, poll_id):
    """Supprimer un sondage"""
    try:
        if not ObjectId.is_valid(poll_id):
            return error_response("ID sondage invalide", 400)
        
        db = get_db()
        poll = db.polls.find_one({"_id": ObjectId(poll_id)})
        if not poll:
            return not_found_response("Sondage non trouvé")
        
        event = db.events.find_one({"_id": poll['event_id']})
        
        # Vérifier que l'utilisateur est le créateur ou organisateur
        if poll['created_by'] != ObjectId(current_user['_id']) and ObjectId(current_user['_id']) not in event.get('organizers', []):
            return error_response("Seul le créateur ou un organisateur peut supprimer ce sondage", 403)
        
        db.polls.delete_one({"_id": ObjectId(poll_id)})
        
        return success_response(None, "Sondage supprimé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@polls_bp.route('/<poll_id>/respond', methods=['POST'])
@token_required
def respond_to_poll(current_user, poll_id):
    """Répondre à un sondage"""
    try:
        if not ObjectId.is_valid(poll_id):
            return error_response("ID sondage invalide", 400)
        
        data = request.get_json()
        is_valid, errors = validate_poll_response(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        poll = db.polls.find_one({"_id": ObjectId(poll_id)})
        if not poll:
            return not_found_response("Sondage non trouvé")
        
        event = db.events.find_one({"_id": poll['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        # Vérifier si l'utilisateur a déjà répondu
        if not poll.get('allow_multiple_votes', False):
            existing = [r for r in poll.get('responses', []) if r['user_id'] == ObjectId(current_user['_id'])]
            if existing:
                return error_response("Vous avez déjà répondu à ce sondage", 400)
        
        response = {
            "user_id": ObjectId(current_user['_id']),
            "user_name": f"{current_user['first_name']} {current_user['last_name']}",
            "responses": data['responses'],
            "created_at": datetime.utcnow()
        }
        
        db.polls.update_one(
            {"_id": ObjectId(poll_id)},
            {"$push": {"responses": response}}
        )
        
        return created_response(response, "Réponse enregistrée avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@polls_bp.route('/<poll_id>/results', methods=['GET'])
@token_required
def get_poll_results(current_user, poll_id):
    """Obtenir les résultats d'un sondage"""
    try:
        if not ObjectId.is_valid(poll_id):
            return error_response("ID sondage invalide", 400)
        
        db = get_db()
        poll = db.polls.find_one({"_id": ObjectId(poll_id)})
        if not poll:
            return not_found_response("Sondage non trouvé")
        
        event = db.events.find_one({"_id": poll['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        # Calculer les statistiques
        results = []
        for q_index, question in enumerate(poll['questions']):
            question_results = {
                "question": question['question'],
                "options": []
            }
            
            # Compter les votes pour chaque option
            for o_index, option in enumerate(question['options']):
                count = 0
                for response in poll.get('responses', []):
                    for r in response['responses']:
                        if r.get('question_index') == q_index and r.get('option_index') == o_index:
                            count += 1
                
                question_results['options'].append({
                    "option": option,
                    "votes": count
                })
            
            results.append(question_results)
        
        return success_response({
            "poll": poll,
            "total_responses": len(poll.get('responses', [])),
            "results": results
        })
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)