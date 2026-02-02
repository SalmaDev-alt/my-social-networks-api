from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required
from validators import validate_carpooling_create, validate_carpooling_update, validate_carpooling_booking

carpooling_bp = Blueprint('carpooling', __name__, url_prefix='/api/carpooling')

@carpooling_bp.route('', methods=['POST'])
@token_required
def create_carpooling_offer(current_user):
    """Créer une offre de covoiturage"""
    try:
        data = request.get_json()
        is_valid, errors = validate_carpooling_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(data['event_id'])})
        if not event:
            return not_found_response("Événement non trouvé")
        
        if not event.get('has_carpooling'):
            return error_response("Le covoiturage n'est pas activé pour cet événement", 400)
        
        if ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Vous devez participer à l'événement", 403)
        
        offer_data = {
            "departure_location": data['departure_location'],
            "departure_time": datetime.fromisoformat(data['departure_time'].replace('Z', '+00:00')),
            "price": data['price'],
            "available_seats": data['available_seats'],
            "total_seats": data['available_seats'],  # Garder le total initial
            "max_time_difference": data['max_time_difference'],
            "event_id": ObjectId(data['event_id']),
            "driver_id": ObjectId(current_user['_id']),
            "driver_name": f"{current_user['first_name']} {current_user['last_name']}",
            "passengers": [],
            "notes": data.get('notes'),
            "created_at": datetime.utcnow()
        }
        
        result = db.carpooling.insert_one(offer_data)
        offer = db.carpooling.find_one({"_id": result.inserted_id})
        
        return created_response(offer, "Offre de covoiturage créée avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@carpooling_bp.route('/event/<event_id>', methods=['GET'])
@token_required
def get_event_carpooling_offers(current_user, event_id):
    """Récupérer les offres de covoiturage d'un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return not_found_response("Événement non trouvé")
        
        if ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        offers = list(db.carpooling.find({"event_id": ObjectId(event_id)}).sort("departure_time", 1))
        return success_response({"carpooling_offers": offers})
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@carpooling_bp.route('/<offer_id>', methods=['GET'])
@token_required
def get_carpooling_offer(current_user, offer_id):
    """Récupérer une offre par son ID"""
    try:
        if not ObjectId.is_valid(offer_id):
            return error_response("ID offre invalide", 400)
        
        db = get_db()
        offer = db.carpooling.find_one({"_id": ObjectId(offer_id)})
        if not offer:
            return not_found_response("Offre non trouvée")
        
        event = db.events.find_one({"_id": offer['event_id']})
        if ObjectId(current_user['_id']) not in event['participants']:
            return error_response("Accès non autorisé", 403)
        
        return success_response(offer)
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@carpooling_bp.route('/<offer_id>', methods=['PUT'])
@token_required
def update_carpooling_offer(current_user, offer_id):
    """Mettre à jour une offre"""
    try:
        if not ObjectId.is_valid(offer_id):
            return error_response("ID offre invalide", 400)
        
        data = request.get_json()
        is_valid, errors = validate_carpooling_update(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        offer = db.carpooling.find_one({"_id": ObjectId(offer_id)})
        if not offer:
            return not_found_response("Offre non trouvée")
        
        if offer['driver_id'] != ObjectId(current_user['_id']):
            return error_response("Vous ne pouvez modifier que vos propres offres", 403)
        
        # Vérifier que le nombre de places disponibles n'est pas inférieur aux réservations
        if 'available_seats' in data:
            seats_booked = sum(p.get('seats_booked', 1) for p in offer.get('passengers', []))
            if data['available_seats'] < 0:
                return error_response("Le nombre de places disponibles ne peut pas être négatif", 400)
        
        data['updated_at'] = datetime.utcnow()
        
        db.carpooling.update_one({"_id": ObjectId(offer_id)}, {"$set": data})
        updated_offer = db.carpooling.find_one({"_id": ObjectId(offer_id)})
        
        return success_response(updated_offer, "Offre mise à jour avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@carpooling_bp.route('/<offer_id>/book', methods=['POST'])
@token_required
def book_carpooling(current_user, offer_id):
    """Réserver une place dans un covoiturage"""
    try:
        if not ObjectId.is_valid(offer_id):
            return error_response("ID offre invalide", 400)
        
        data = request.get_json()
        is_valid, errors = validate_carpooling_booking(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        offer = db.carpooling.find_one({"_id": ObjectId(offer_id)})
        if not offer:
            return not_found_response("Offre non trouvée")
        
        if offer['driver_id'] == ObjectId(current_user['_id']):
            return error_response("Vous ne pouvez pas réserver votre propre offre", 400)
        
        if offer['available_seats'] < data['seats_requested']:
            return error_response(f"Pas assez de places disponibles (seulement {offer['available_seats']} places)", 400)
        
        # Vérifier si l'utilisateur a déjà réservé
        for passenger in offer.get('passengers', []):
            if passenger['user_id'] == ObjectId(current_user['_id']):
                return error_response("Vous avez déjà réservé une place dans ce covoiturage", 400)
        
        passenger_info = {
            "user_id": ObjectId(current_user['_id']),
            "user_name": f"{current_user['first_name']} {current_user['last_name']}",
            "seats_booked": data['seats_requested'],
            "booked_at": datetime.utcnow()
        }
        
        db.carpooling.update_one(
            {"_id": ObjectId(offer_id)},
            {
                "$push": {"passengers": passenger_info},
                "$inc": {"available_seats": -data['seats_requested']}
            }
        )
        
        return created_response(passenger_info, "Réservation effectuée avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@carpooling_bp.route('/<offer_id>/cancel', methods=['POST'])
@token_required
def cancel_carpooling_booking(current_user, offer_id):
    """Annuler sa réservation"""
    try:
        if not ObjectId.is_valid(offer_id):
            return error_response("ID offre invalide", 400)
        
        db = get_db()
        offer = db.carpooling.find_one({"_id": ObjectId(offer_id)})
        if not offer:
            return not_found_response("Offre non trouvée")
        
        # Trouver la réservation de l'utilisateur
        passenger = None
        for p in offer.get('passengers', []):
            if p['user_id'] == ObjectId(current_user['_id']):
                passenger = p
                break
        
        if not passenger:
            return error_response("Vous n'avez pas de réservation pour ce covoiturage", 400)
        
        # Annuler la réservation
        db.carpooling.update_one(
            {"_id": ObjectId(offer_id)},
            {
                "$pull": {"passengers": {"user_id": ObjectId(current_user['_id'])}},
                "$inc": {"available_seats": passenger['seats_booked']}
            }
        )
        
        return success_response(None, "Réservation annulée avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@carpooling_bp.route('/<offer_id>', methods=['DELETE'])
@token_required
def delete_carpooling_offer(current_user, offer_id):
    """Supprimer une offre"""
    try:
        if not ObjectId.is_valid(offer_id):
            return error_response("ID offre invalide", 400)
        
        db = get_db()
        offer = db.carpooling.find_one({"_id": ObjectId(offer_id)})
        if not offer:
            return not_found_response("Offre non trouvée")
        
        # Vérifier que l'utilisateur est le conducteur ou organisateur
        event = db.events.find_one({"_id": offer['event_id']})
        if offer['driver_id'] != ObjectId(current_user['_id']) and ObjectId(current_user['_id']) not in event.get('organizers', []):
            return error_response("Vous ne pouvez supprimer que vos propres offres", 403)
        
        # Vérifier s'il y a des passagers
        if len(offer.get('passengers', [])) > 0:
            return error_response("Impossible de supprimer une offre avec des réservations. Annulez d'abord toutes les réservations.", 400)
        
        db.carpooling.delete_one({"_id": ObjectId(offer_id)})
        
        return success_response(None, "Offre supprimée avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)