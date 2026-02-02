from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required
from validators import validate_shopping_item_create, validate_shopping_item_update

shopping_bp = Blueprint('shopping', __name__, url_prefix='/api/shopping')

@shopping_bp.route('', methods=['POST'])
@token_required
def create_shopping_item(current_user):
    """Créer un item de shopping list"""
    try:
        data = request.get_json()
        is_valid, errors = validate_shopping_item_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(data['event_id'])})
        if not event:
            return not_found_response("Événement non trouvé")
        
        if not event.get('has_shopping_list'):
            return error_response("La shopping list n'est pas activée pour cet événement", 400)
        
        if ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Vous devez participer à l'événement", 403)
        
        # Vérifier l'unicité du nom par événement
        existing = db.shopping_items.find_one({
            "event_id": ObjectId(data['event_id']),
            "name": data['name']
        })
        if existing:
            return error_response("Cet item existe déjà pour cet événement", 400)
        
        item_data = {
            "name": data['name'],
            "quantity": data['quantity'],
            "arrival_time": datetime.fromisoformat(data['arrival_time'].replace('Z', '+00:00')),
            "event_id": ObjectId(data['event_id']),
            "user_id": ObjectId(current_user['_id']),
            "user_name": f"{current_user['first_name']} {current_user['last_name']}",
            "notes": data.get('notes'),
            "created_at": datetime.utcnow()
        }
        
        result = db.shopping_items.insert_one(item_data)
        item = db.shopping_items.find_one({"_id": result.inserted_id})
        
        return created_response(item, "Item ajouté avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@shopping_bp.route('/event/<event_id>', methods=['GET'])
@token_required
def get_event_shopping_items(current_user, event_id):
    """Récupérer la shopping list d'un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return not_found_response("Événement non trouvé")
        
        if ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        items = list(db.shopping_items.find({"event_id": ObjectId(event_id)}).sort("arrival_time", 1))
        return success_response({"shopping_items": items})
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@shopping_bp.route('/<item_id>', methods=['GET'])
@token_required
def get_shopping_item(current_user, item_id):
    """Récupérer un item par son ID"""
    try:
        if not ObjectId.is_valid(item_id):
            return error_response("ID item invalide", 400)
        
        db = get_db()
        item = db.shopping_items.find_one({"_id": ObjectId(item_id)})
        if not item:
            return not_found_response("Item non trouvé")
        
        event = db.events.find_one({"_id": item['event_id']})
        if ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        return success_response(item)
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@shopping_bp.route('/<item_id>', methods=['PUT'])
@token_required
def update_shopping_item(current_user, item_id):
    """Mettre à jour un item"""
    try:
        if not ObjectId.is_valid(item_id):
            return error_response("ID item invalide", 400)
        
        data = request.get_json()
        is_valid, errors = validate_shopping_item_update(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        item = db.shopping_items.find_one({"_id": ObjectId(item_id)})
        if not item:
            return not_found_response("Item non trouvé")
        
        if item['user_id'] != ObjectId(current_user['_id']):
            return error_response("Vous ne pouvez modifier que vos propres items", 403)
        
        if 'arrival_time' in data:
            data['arrival_time'] = datetime.fromisoformat(data['arrival_time'].replace('Z', '+00:00'))
        
        data['updated_at'] = datetime.utcnow()
        
        db.shopping_items.update_one({"_id": ObjectId(item_id)}, {"$set": data})
        updated_item = db.shopping_items.find_one({"_id": ObjectId(item_id)})
        
        return success_response(updated_item, "Item mis à jour avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@shopping_bp.route('/<item_id>', methods=['DELETE'])
@token_required
def delete_shopping_item(current_user, item_id):
    """Supprimer un item"""
    try:
        if not ObjectId.is_valid(item_id):
            return error_response("ID item invalide", 400)
        
        db = get_db()
        item = db.shopping_items.find_one({"_id": ObjectId(item_id)})
        if not item:
            return not_found_response("Item non trouvé")
        
        # Vérifier que l'utilisateur est le créateur ou organisateur
        event = db.events.find_one({"_id": item['event_id']})
        if item['user_id'] != ObjectId(current_user['_id']) and ObjectId(current_user['_id']) not in event.get('organizers', []):
            return error_response("Vous ne pouvez supprimer que vos propres items", 403)
        
        db.shopping_items.delete_one({"_id": ObjectId(item_id)})
        
        return success_response(None, "Item supprimé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)