from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required, optional_token
from validators import validate_group_create, validate_group_update

groups_bp = Blueprint('groups', __name__, url_prefix='/api/groups')

@groups_bp.route('', methods=['POST'])
@token_required
def create_group(current_user):
    """Créer un nouveau groupe"""
    try:
        data = request.get_json()
        
        is_valid, errors = validate_group_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        
        group_data = {
            "name": data['name'],
            "description": data['description'],
            "icon": data.get('icon'),
            "cover_photo": data.get('cover_photo'),
            "group_type": data['group_type'],
            "allow_members_to_post": data.get('allow_members_to_post', True),
            "allow_members_to_create_events": data.get('allow_members_to_create_events', True),
            "administrators": [ObjectId(current_user['_id'])],
            "members": [ObjectId(current_user['_id'])],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        if data.get('members'):
            for member_id in data['members']:
                if ObjectId.is_valid(member_id) and ObjectId(member_id) not in group_data['members']:
                    group_data['members'].append(ObjectId(member_id))
        
        result = db.groups.insert_one(group_data)
        
        # Créer le fil de discussion du groupe
        db.discussions.insert_one({
            "event_id": None,
            "group_id": result.inserted_id,
            "messages": [],
            "created_at": datetime.utcnow()
        })
        
        group = db.groups.find_one({"_id": result.inserted_id})
        
        return created_response(group, "Groupe créé avec succès")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@groups_bp.route('', methods=['GET'])
@optional_token
def get_groups(current_user):
    """Récupérer la liste des groupes"""
    try:
        db = get_db()
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        skip = (page - 1) * per_page
        
        query = {}
        
        if current_user:
            query = {
                "$or": [
                    {"group_type": "public"},
                    {"members": ObjectId(current_user['_id'])}
                ]
            }
        else:
            query = {"group_type": "public"}
        
        groups = list(db.groups.find(query).skip(skip).limit(per_page))
        total = db.groups.count_documents(query)
        
        return success_response({
            "groups": groups,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@groups_bp.route('/<group_id>', methods=['GET'])
@optional_token
def get_group(current_user, group_id):
    """Récupérer un groupe par son ID"""
    try:
        if not ObjectId.is_valid(group_id):
            return error_response("ID groupe invalide", 400)
        
        db = get_db()
        group = db.groups.find_one({"_id": ObjectId(group_id)})
        
        if not group:
            return not_found_response("Groupe non trouvé")
        
        # Vérifier l'accès pour les groupes privés/secrets
        if group['group_type'] in ['private', 'secret']:
            if not current_user or ObjectId(current_user['_id']) not in group['members']:
                return error_response("Accès non autorisé", 403)
        
        return success_response(group)
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@groups_bp.route('/<group_id>', methods=['PUT'])
@token_required
def update_group(current_user, group_id):
    """Mettre à jour un groupe"""
    try:
        if not ObjectId.is_valid(group_id):
            return error_response("ID groupe invalide", 400)
        
        db = get_db()
        group = db.groups.find_one({"_id": ObjectId(group_id)})
        
        if not group:
            return not_found_response("Groupe non trouvé")
        
        if ObjectId(current_user['_id']) not in group['administrators']:
            return error_response("Seuls les administrateurs peuvent modifier le groupe", 403)
        
        data = request.get_json()
        
        is_valid, errors = validate_group_update(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        data['updated_at'] = datetime.utcnow()
        
        db.groups.update_one({"_id": ObjectId(group_id)}, {"$set": data})
        
        updated_group = db.groups.find_one({"_id": ObjectId(group_id)})
        
        return success_response(updated_group, "Groupe mis à jour avec succès")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@groups_bp.route('/<group_id>/join', methods=['POST'])
@token_required
def join_group(current_user, group_id):
    """Rejoindre un groupe"""
    try:
        if not ObjectId.is_valid(group_id):
            return error_response("ID groupe invalide", 400)
        
        db = get_db()
        group = db.groups.find_one({"_id": ObjectId(group_id)})
        
        if not group:
            return not_found_response("Groupe non trouvé")
        
        if group['group_type'] == 'secret':
            return error_response("Impossible de rejoindre un groupe secret sans invitation", 403)
        
        user_id = ObjectId(current_user['_id'])
        
        if user_id in group['members']:
            return error_response("Vous êtes déjà membre de ce groupe", 400)
        
        db.groups.update_one(
            {"_id": ObjectId(group_id)},
            {"$push": {"members": user_id}}
        )
        
        return success_response(None, "Vous êtes maintenant membre du groupe")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@groups_bp.route('/<group_id>/leave', methods=['POST'])
@token_required
def leave_group(current_user, group_id):
    """Quitter un groupe"""
    try:
        if not ObjectId.is_valid(group_id):
            return error_response("ID groupe invalide", 400)
        
        db = get_db()
        group = db.groups.find_one({"_id": ObjectId(group_id)})
        
        if not group:
            return not_found_response("Groupe non trouvé")
        
        user_id = ObjectId(current_user['_id'])
        
        if user_id in group['administrators'] and len(group['administrators']) == 1:
            return error_response("Le dernier administrateur ne peut pas quitter le groupe", 400)
        
        db.groups.update_one(
            {"_id": ObjectId(group_id)},
            {"$pull": {"members": user_id, "administrators": user_id}}
        )
        
        return success_response(None, "Vous avez quitté le groupe")
        
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)