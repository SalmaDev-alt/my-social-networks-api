from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required
from validators import validate_album_create, validate_photo_create, validate_comment_create

albums_bp = Blueprint('albums', __name__, url_prefix='/api/albums')

@albums_bp.route('', methods=['POST'])
@token_required
def create_album(current_user):
    """Créer un album photo"""
    try:
        data = request.get_json()
        is_valid, errors = validate_album_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(data['event_id'])})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        album_data = {
            "name": data['name'],
            "description": data.get('description'),
            "event_id": ObjectId(data['event_id']),
            "created_by": ObjectId(current_user['_id']),
            "created_at": datetime.utcnow()
        }
        
        result = db.albums.insert_one(album_data)
        album = db.albums.find_one({"_id": result.inserted_id})
        
        return created_response(album, "Album créé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/event/<event_id>', methods=['GET'])
@token_required
def get_event_albums(current_user, event_id):
    """Récupérer les albums d'un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        albums = list(db.albums.find({"event_id": ObjectId(event_id)}))
        return success_response({"albums": albums})
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/<album_id>', methods=['GET'])
@token_required
def get_album(current_user, album_id):
    """Récupérer un album par son ID"""
    try:
        if not ObjectId.is_valid(album_id):
            return error_response("ID album invalide", 400)
        
        db = get_db()
        album = db.albums.find_one({"_id": ObjectId(album_id)})
        if not album:
            return not_found_response("Album non trouvé")
        
        event = db.events.find_one({"_id": album['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        return success_response(album)
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/<album_id>', methods=['DELETE'])
@token_required
def delete_album(current_user, album_id):
    """Supprimer un album"""
    try:
        if not ObjectId.is_valid(album_id):
            return error_response("ID album invalide", 400)
        
        db = get_db()
        album = db.albums.find_one({"_id": ObjectId(album_id)})
        if not album:
            return not_found_response("Album non trouvé")
        
        # Vérifier que l'utilisateur est le créateur de l'album ou organisateur de l'événement
        event = db.events.find_one({"_id": album['event_id']})
        if album['created_by'] != ObjectId(current_user['_id']) and ObjectId(current_user['_id']) not in event.get('organizers', []):
            return error_response("Seul le créateur ou un organisateur peut supprimer cet album", 403)
        
        # Supprimer toutes les photos de l'album
        db.photos.delete_many({"album_id": ObjectId(album_id)})
        
        # Supprimer l'album
        db.albums.delete_one({"_id": ObjectId(album_id)})
        
        return success_response(None, "Album supprimé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/<album_id>/photos', methods=['POST'])
@token_required
def add_photo(current_user, album_id):
    """Ajouter une photo à un album"""
    try:
        if not ObjectId.is_valid(album_id):
            return error_response("ID album invalide", 400)
        
        data = request.get_json()
        data['album_id'] = album_id
        
        is_valid, errors = validate_photo_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        album = db.albums.find_one({"_id": ObjectId(album_id)})
        if not album:
            return not_found_response("Album non trouvé")
        
        event = db.events.find_one({"_id": album['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        photo_data = {
            "url": data['url'],
            "caption": data.get('caption'),
            "album_id": ObjectId(album_id),
            "posted_by": ObjectId(current_user['_id']),
            "posted_by_name": f"{current_user['first_name']} {current_user['last_name']}",
            "comments": [],
            "created_at": datetime.utcnow()
        }
        
        result = db.photos.insert_one(photo_data)
        photo = db.photos.find_one({"_id": result.inserted_id})
        
        return created_response(photo, "Photo ajoutée avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/<album_id>/photos', methods=['GET'])
@token_required
def get_album_photos(current_user, album_id):
    """Récupérer les photos d'un album"""
    try:
        if not ObjectId.is_valid(album_id):
            return error_response("ID album invalide", 400)
        
        db = get_db()
        album = db.albums.find_one({"_id": ObjectId(album_id)})
        if not album:
            return not_found_response("Album non trouvé")
        
        event = db.events.find_one({"_id": album['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        photos = list(db.photos.find({"album_id": ObjectId(album_id)}).sort("created_at", -1))
        return success_response({"photos": photos})
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/photos/<photo_id>', methods=['GET'])
@token_required
def get_photo(current_user, photo_id):
    """Récupérer une photo par son ID"""
    try:
        if not ObjectId.is_valid(photo_id):
            return error_response("ID photo invalide", 400)
        
        db = get_db()
        photo = db.photos.find_one({"_id": ObjectId(photo_id)})
        if not photo:
            return not_found_response("Photo non trouvée")
        
        album = db.albums.find_one({"_id": photo['album_id']})
        event = db.events.find_one({"_id": album['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        return success_response(photo)
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/photos/<photo_id>', methods=['DELETE'])
@token_required
def delete_photo(current_user, photo_id):
    """Supprimer une photo"""
    try:
        if not ObjectId.is_valid(photo_id):
            return error_response("ID photo invalide", 400)
        
        db = get_db()
        photo = db.photos.find_one({"_id": ObjectId(photo_id)})
        if not photo:
            return not_found_response("Photo non trouvée")
        
        # Vérifier que l'utilisateur est le créateur de la photo ou organisateur
        album = db.albums.find_one({"_id": photo['album_id']})
        event = db.events.find_one({"_id": album['event_id']})
        
        if photo['posted_by'] != ObjectId(current_user['_id']) and ObjectId(current_user['_id']) not in event.get('organizers', []):
            return error_response("Seul le créateur ou un organisateur peut supprimer cette photo", 403)
        
        db.photos.delete_one({"_id": ObjectId(photo_id)})
        
        return success_response(None, "Photo supprimée avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/photos/<photo_id>/comments', methods=['POST'])
@token_required
def add_comment(current_user, photo_id):
    """Ajouter un commentaire sur une photo"""
    try:
        if not ObjectId.is_valid(photo_id):
            return error_response("ID photo invalide", 400)
        
        data = request.get_json()
        is_valid, errors = validate_comment_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        photo = db.photos.find_one({"_id": ObjectId(photo_id)})
        if not photo:
            return not_found_response("Photo non trouvée")
        
        album = db.albums.find_one({"_id": photo['album_id']})
        event = db.events.find_one({"_id": album['event_id']})
        if not event or ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        comment = {
            "_id": ObjectId(),
            "author_id": ObjectId(current_user['_id']),
            "author_name": f"{current_user['first_name']} {current_user['last_name']}",
            "content": data['content'],
            "created_at": datetime.utcnow()
        }
        
        db.photos.update_one(
            {"_id": ObjectId(photo_id)},
            {"$push": {"comments": comment}}
        )
        
        return created_response(comment, "Commentaire ajouté avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@albums_bp.route('/photos/<photo_id>/comments/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, photo_id, comment_id):
    """Supprimer un commentaire"""
    try:
        if not ObjectId.is_valid(photo_id) or not ObjectId.is_valid(comment_id):
            return error_response("ID invalide", 400)
        
        db = get_db()
        photo = db.photos.find_one({"_id": ObjectId(photo_id)})
        if not photo:
            return not_found_response("Photo non trouvée")
        
        # Trouver le commentaire
        comment = None
        for c in photo.get('comments', []):
            if str(c['_id']) == comment_id:
                comment = c
                break
        
        if not comment:
            return not_found_response("Commentaire non trouvé")
        
        # Vérifier que l'utilisateur est l'auteur du commentaire ou organisateur
        album = db.albums.find_one({"_id": photo['album_id']})
        event = db.events.find_one({"_id": album['event_id']})
        
        if comment['author_id'] != ObjectId(current_user['_id']) and ObjectId(current_user['_id']) not in event.get('organizers', []):
            return error_response("Seul l'auteur ou un organisateur peut supprimer ce commentaire", 403)
        
        db.photos.update_one(
            {"_id": ObjectId(photo_id)},
            {"$pull": {"comments": {"_id": ObjectId(comment_id)}}}
        )
        
        return success_response(None, "Commentaire supprimé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)