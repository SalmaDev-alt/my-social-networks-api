from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required
from validators import validate_message_create

discussions_bp = Blueprint('discussions', __name__, url_prefix='/api/discussions')

@discussions_bp.route('/event/<event_id>/messages', methods=['GET'])
@token_required
def get_event_messages(current_user, event_id):
    """Récupérer les messages d'un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        
        # Vérifier l'accès à l'événement
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        discussion = db.discussions.find_one({"event_id": ObjectId(event_id)})
        
        if not discussion:
            return success_response({"messages": []})
        
        return success_response({"messages": discussion.get('messages', [])})
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@discussions_bp.route('/group/<group_id>/messages', methods=['GET'])
@token_required
def get_group_messages(current_user, group_id):
    """Récupérer les messages d'un groupe"""
    try:
        if not ObjectId.is_valid(group_id):
            return error_response("ID groupe invalide", 400)
        
        db = get_db()
        
        # Vérifier l'accès au groupe
        group = db.groups.find_one({"_id": ObjectId(group_id)})
        if not group or ObjectId(current_user['_id']) not in group['members']:
            return error_response("Accès non autorisé", 403)
        
        discussion = db.discussions.find_one({"group_id": ObjectId(group_id)})
        
        if not discussion:
            return success_response({"messages": []})
        
        return success_response({"messages": discussion.get('messages', [])})
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@discussions_bp.route('/event/<event_id>/messages', methods=['POST'])
@token_required
def post_event_message(current_user, event_id):
    """Poster un message dans un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        data = request.get_json()
        
        is_valid, errors = validate_message_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        
        # Vérifier l'accès
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        message = {
            "_id": ObjectId(),
            "author_id": ObjectId(current_user['_id']),
            "author_name": f"{current_user['first_name']} {current_user['last_name']}",
            "content": data['content'],
            "parent_message_id": ObjectId(data['parent_message_id']) if data.get('parent_message_id') else None,
            "created_at": datetime.utcnow()
        }
        
        db.discussions.update_one(
            {"event_id": ObjectId(event_id)},
            {"$push": {"messages": message}}
        )
        
        return created_response(message, "Message posté avec succès")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@discussions_bp.route('/group/<group_id>/messages', methods=['POST'])
@token_required
def post_group_message(current_user, group_id):
    """Poster un message dans un groupe"""
    try:
        if not ObjectId.is_valid(group_id):
            return error_response("ID groupe invalide", 400)
        
        data = request.get_json()
        
        is_valid, errors = validate_message_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        
        # Vérifier l'accès et les permissions
        group = db.groups.find_one({"_id": ObjectId(group_id)})
        if not group or ObjectId(current_user['_id']) not in group['members']:
            return error_response("Accès non autorisé", 403)
        
        if not group['allow_members_to_post'] and ObjectId(current_user['_id']) not in group['administrators']:
            return error_response("Seuls les administrateurs peuvent poster dans ce groupe", 403)
        
        message = {
            "_id": ObjectId(),
            "author_id": ObjectId(current_user['_id']),
            "author_name": f"{current_user['first_name']} {current_user['last_name']}",
            "content": data['content'],
            "parent_message_id": ObjectId(data['parent_message_id']) if data.get('parent_message_id') else None,
            "created_at": datetime.utcnow()
        }
        
        db.discussions.update_one(
            {"group_id": ObjectId(group_id)},
            {"$push": {"messages": message}}
        )
        
        return created_response(message, "Message posté avec succès")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)