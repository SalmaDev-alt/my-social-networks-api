from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required, optional_token
from validators import validate_event_create, validate_event_update

events_bp = Blueprint('events', __name__, url_prefix='/api/events')

@events_bp.route('', methods=['POST'])
@token_required
def create_event(current_user):
    """Créer un nouvel événement"""
    try:
        data = request.get_json()
        
        # Validation
        is_valid, errors = validate_event_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        
        # Préparer les données
        event_data = {
            "name": data['name'],
            "description": data['description'],
            "start_date": datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
            "end_date": datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')),
            "location": data['location'],
            "cover_photo": data.get('cover_photo'),
            "is_private": data.get('is_private', False),
            "organizers": [ObjectId(current_user['_id'])],  # Créateur = organisateur
            "participants": [ObjectId(current_user['_id'])],  # Créateur = participant
            "group_id": ObjectId(data['group_id']) if data.get('group_id') else None,
            "has_ticketing": data.get('has_ticketing', False),
            "has_shopping_list": data.get('has_shopping_list', False),
            "has_carpooling": data.get('has_carpooling', False),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Ajouter d'autres organisateurs si spécifiés
        if data.get('organizers'):
            for org_id in data['organizers']:
                if ObjectId.is_valid(org_id) and ObjectId(org_id) not in event_data['organizers']:
                    event_data['organizers'].append(ObjectId(org_id))
        
        # Ajouter des participants si spécifiés
        if data.get('participants'):
            for part_id in data['participants']:
                if ObjectId.is_valid(part_id) and ObjectId(part_id) not in event_data['participants']:
                    event_data['participants'].append(ObjectId(part_id))
        
        result = db.events.insert_one(event_data)
        
        # Créer automatiquement un fil de discussion pour l'événement
        db.discussions.insert_one({
            "event_id": result.inserted_id,
            "group_id": None,
            "messages": [],
            "created_at": datetime.utcnow()
        })
        
        event = db.events.find_one({"_id": result.inserted_id})
        
        return created_response(event, "Événement créé avec succès")
        
    except Exception as e:
        return error_response(f"Erreur lors de la création: {str(e)}", 500)

@events_bp.route('', methods=['GET'])
@optional_token
def get_events(current_user):
    """Récupérer la liste des événements"""
    try:
        db = get_db()
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        skip = (page - 1) * per_page
        
        # Filtres
        query = {}
        
        # Si utilisateur connecté, montrer tous les événements publics + ses événements privés
        if current_user:
            query = {
                "$or": [
                    {"is_private": False},
                    {"participants": ObjectId(current_user['_id'])}
                ]
            }
        else:
            # Sinon, uniquement les événements publics
            query = {"is_private": False}
        
        # Filtre par groupe
        if request.args.get('group_id'):
            query['group_id'] = ObjectId(request.args.get('group_id'))
        
        events = list(db.events.find(query).skip(skip).limit(per_page).sort("start_date", 1))
        total = db.events.count_documents(query)
        
        return success_response({
            "events": events,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return error_response(f"Erreur lors de la récupération: {str(e)}", 500)

@events_bp.route('/<event_id>', methods=['GET'])
@optional_token
def get_event(current_user, event_id):
    """Récupérer un événement par son ID"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        
        if not event:
            return not_found_response("Événement non trouvé")
        
        # Vérifier l'accès pour les événements privés
        if event['is_private']:
            if not current_user or ObjectId(current_user['_id']) not in event['participants']:
                return error_response("Accès non autorisé à cet événement privé", 403)
        
        return success_response(event)
        
    except Exception as e:
        return error_response(f"Erreur lors de la récupération: {str(e)}", 500)

@events_bp.route('/<event_id>', methods=['PUT'])
@token_required
def update_event(current_user, event_id):
    """Mettre à jour un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        
        if not event:
            return not_found_response("Événement non trouvé")
        
        # Vérifier que l'utilisateur est organisateur
        if ObjectId(current_user['_id']) not in event['organizers']:
            return error_response("Seuls les organisateurs peuvent modifier l'événement", 403)
        
        data = request.get_json()
        
        # Validation
        is_valid, errors = validate_event_update(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        # Convertir les dates si présentes
        if 'start_date' in data:
            data['start_date'] = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        if 'end_date' in data:
            data['end_date'] = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        data['updated_at'] = datetime.utcnow()
        
        db.events.update_one({"_id": ObjectId(event_id)}, {"$set": data})
        
        updated_event = db.events.find_one({"_id": ObjectId(event_id)})
        
        return success_response(updated_event, "Événement mis à jour avec succès")
        
    except Exception as e:
        return error_response(f"Erreur lors de la mise à jour: {str(e)}", 500)

@events_bp.route('/<event_id>', methods=['DELETE'])
@token_required
def delete_event(current_user, event_id):
    """Supprimer un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        
        if not event:
            return not_found_response("Événement non trouvé")
        
        # Vérifier que l'utilisateur est organisateur
        if ObjectId(current_user['_id']) not in event['organizers']:
            return error_response("Seuls les organisateurs peuvent supprimer l'événement", 403)
        
        db.events.delete_one({"_id": ObjectId(event_id)})
        
        return success_response(None, "Événement supprimé avec succès")
        
    except Exception as e:
        return error_response(f"Erreur lors de la suppression: {str(e)}", 500)

@events_bp.route('/<event_id>/join', methods=['POST'])
@token_required
def join_event(current_user, event_id):
    """Rejoindre un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        
        if not event:
            return not_found_response("Événement non trouvé")
        
        user_id = ObjectId(current_user['_id'])
        
        # Vérifier si l'utilisateur est déjà participant
        if user_id in event['participants']:
            return error_response("Vous participez déjà à cet événement", 400)
        
        # Ajouter l'utilisateur aux participants
        db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$push": {"participants": user_id}}
        )
        
        return success_response(None, "Vous participez maintenant à l'événement")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@events_bp.route('/<event_id>/leave', methods=['POST'])
@token_required
def leave_event(current_user, event_id):
    """Quitter un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        
        if not event:
            return not_found_response("Événement non trouvé")
        
        user_id = ObjectId(current_user['_id'])
        
        # Vérifier si l'utilisateur est organisateur
        if user_id in event['organizers'] and len(event['organizers']) == 1:
            return error_response("Le dernier organisateur ne peut pas quitter l'événement", 400)
        
        # Retirer l'utilisateur des participants et organisateurs
        db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$pull": {"participants": user_id, "organizers": user_id}}
        )
        
        return success_response(None, "Vous avez quitté l'événement")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)