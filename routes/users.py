from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response
from middleware import token_required
from validators import validate_user_update

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('', methods=['GET'])
@token_required
def get_users(current_user):
    """Récupérer la liste des utilisateurs"""
    try:
        db = get_db()
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        skip = (page - 1) * per_page
        
        # Recherche optionnelle
        search = request.args.get('search', '')
        query = {}
        if search:
            query = {
                "$or": [
                    {"first_name": {"$regex": search, "$options": "i"}},
                    {"last_name": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}}
                ]
            }
        
        users = list(db.users.find(query, {"password": 0}).skip(skip).limit(per_page))
        total = db.users.count_documents(query)
        
        return success_response({
            "users": users,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return error_response(f"Erreur lors de la récupération des utilisateurs: {str(e)}", 500)

@users_bp.route('/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """Récupérer un utilisateur par son ID"""
    try:
        if not ObjectId.is_valid(user_id):
            return error_response("ID utilisateur invalide", 400)
        
        db = get_db()
        user = db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
        
        if not user:
            return not_found_response("Utilisateur non trouvé")
        
        return success_response(user)
        
    except Exception as e:
        return error_response(f"Erreur lors de la récupération de l'utilisateur: {str(e)}", 500)

@users_bp.route('/<user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """Mettre à jour un utilisateur"""
    try:
        if not ObjectId.is_valid(user_id):
            return error_response("ID utilisateur invalide", 400)
        
        # Vérifier que l'utilisateur modifie son propre profil
        if str(current_user['_id']) != user_id:
            return error_response("Vous ne pouvez modifier que votre propre profil", 403)
        
        data = request.get_json()
        
        # Validation
        is_valid, errors = validate_user_update(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        
        # Mettre à jour
        data['updated_at'] = datetime.utcnow()
        result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        
        if result.matched_count == 0:
            return not_found_response("Utilisateur non trouvé")
        
        # Récupérer l'utilisateur mis à jour
        user = db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
        
        return success_response(user, "Utilisateur mis à jour avec succès")
        
    except Exception as e:
        return error_response(f"Erreur lors de la mise à jour: {str(e)}", 500)

@users_bp.route('/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    """Supprimer un utilisateur"""
    try:
        if not ObjectId.is_valid(user_id):
            return error_response("ID utilisateur invalide", 400)
        
        # Vérifier que l'utilisateur supprime son propre profil
        if str(current_user['_id']) != user_id:
            return error_response("Vous ne pouvez supprimer que votre propre profil", 403)
        
        db = get_db()
        
        result = db.users.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return not_found_response("Utilisateur non trouvé")
        
        return success_response(None, "Utilisateur supprimé avec succès")
        
    except Exception as e:
        return error_response(f"Erreur lors de la suppression: {str(e)}", 500)