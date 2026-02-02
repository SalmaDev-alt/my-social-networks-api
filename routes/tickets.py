from flask import Blueprint, request
from bson import ObjectId
from datetime import datetime
from utils import get_db, success_response, error_response, not_found_response, created_response
from middleware import token_required, optional_token
from validators import validate_ticket_type_create, validate_ticket_purchase

tickets_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')

@tickets_bp.route('/types', methods=['POST'])
@token_required
def create_ticket_type(current_user):
    """Créer un type de billet"""
    try:
        data = request.get_json()
        
        # Ajouter event_id au data pour validation
        event_id = data.get('event_id')
        if not event_id or not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide ou manquant", 400)
        
        is_valid, errors = validate_ticket_type_create(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return not_found_response("Événement non trouvé")
        
        if ObjectId(current_user['_id']) not in event['organizers']:
            return error_response("Seuls les organisateurs peuvent créer des types de billets", 403)
        
        if not event.get('has_ticketing'):
            return error_response("La billetterie n'est pas activée pour cet événement", 400)
        
        ticket_type_data = {
            "name": data['name'],
            "price": data['price'],
            "quantity": data['quantity'],
            "remaining": data['quantity'],
            "description": data.get('description'),
            "event_id": ObjectId(event_id),
            "created_by": ObjectId(current_user['_id']),
            "created_at": datetime.utcnow()
        }
        
        result = db.ticket_types.insert_one(ticket_type_data)
        ticket_type = db.ticket_types.find_one({"_id": result.inserted_id})
        
        return created_response(ticket_type, "Type de billet créé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@tickets_bp.route('/types/event/<event_id>', methods=['GET'])
@optional_token
def get_ticket_types(current_user, event_id):
    """Récupérer les types de billets d'un événement"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return not_found_response("Événement non trouvé")
        
        # Vérifier l'accès pour les événements privés
        if event.get('is_private'):
            if not current_user or ObjectId(current_user['_id']) not in event['participants']:
                return error_response("Accès non autorisé à cet événement privé", 403)
        
        ticket_types = list(db.ticket_types.find({"event_id": ObjectId(event_id)}))
        return success_response({"ticket_types": ticket_types})
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@tickets_bp.route('/types/<ticket_type_id>', methods=['GET'])
@optional_token
def get_ticket_type(current_user, ticket_type_id):
    """Récupérer un type de billet par son ID"""
    try:
        if not ObjectId.is_valid(ticket_type_id):
            return error_response("ID type de billet invalide", 400)
        
        db = get_db()
        ticket_type = db.ticket_types.find_one({"_id": ObjectId(ticket_type_id)})
        if not ticket_type:
            return not_found_response("Type de billet non trouvé")
        
        event = db.events.find_one({"_id": ticket_type['event_id']})
        if event.get('is_private'):
            if not current_user or ObjectId(current_user['_id']) not in event['participants']:
                return error_response("Accès non autorisé", 403)
        
        return success_response(ticket_type)
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@tickets_bp.route('/types/<ticket_type_id>', methods=['PUT'])
@token_required
def update_ticket_type(current_user, ticket_type_id):
    """Mettre à jour un type de billet"""
    try:
        if not ObjectId.is_valid(ticket_type_id):
            return error_response("ID type de billet invalide", 400)
        
        data = request.get_json()
        
        db = get_db()
        ticket_type = db.ticket_types.find_one({"_id": ObjectId(ticket_type_id)})
        if not ticket_type:
            return not_found_response("Type de billet non trouvé")
        
        event = db.events.find_one({"_id": ticket_type['event_id']})
        if ObjectId(current_user['_id']) not in event['organizers']:
            return error_response("Seuls les organisateurs peuvent modifier les types de billets", 403)
        
        # Ne pas permettre de réduire la quantité en dessous des billets vendus
        if 'quantity' in data:
            sold = ticket_type['quantity'] - ticket_type['remaining']
            if data['quantity'] < sold:
                return error_response(f"Impossible de réduire la quantité en dessous de {sold} (billets déjà vendus)", 400)
            data['remaining'] = data['quantity'] - sold
        
        data['updated_at'] = datetime.utcnow()
        
        db.ticket_types.update_one({"_id": ObjectId(ticket_type_id)}, {"$set": data})
        updated_ticket_type = db.ticket_types.find_one({"_id": ObjectId(ticket_type_id)})
        
        return success_response(updated_ticket_type, "Type de billet mis à jour avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@tickets_bp.route('/types/<ticket_type_id>', methods=['DELETE'])
@token_required
def delete_ticket_type(current_user, ticket_type_id):
    """Supprimer un type de billet"""
    try:
        if not ObjectId.is_valid(ticket_type_id):
            return error_response("ID type de billet invalide", 400)
        
        db = get_db()
        ticket_type = db.ticket_types.find_one({"_id": ObjectId(ticket_type_id)})
        if not ticket_type:
            return not_found_response("Type de billet non trouvé")
        
        event = db.events.find_one({"_id": ticket_type['event_id']})
        if ObjectId(current_user['_id']) not in event['organizers']:
            return error_response("Seuls les organisateurs peuvent supprimer les types de billets", 403)
        
        # Vérifier s'il y a des billets vendus
        sold = ticket_type['quantity'] - ticket_type['remaining']
        if sold > 0:
            return error_response(f"Impossible de supprimer ce type de billet car {sold} billet(s) ont déjà été vendu(s)", 400)
        
        db.ticket_types.delete_one({"_id": ObjectId(ticket_type_id)})
        
        return success_response(None, "Type de billet supprimé avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@tickets_bp.route('/purchase', methods=['POST'])
def purchase_ticket():
    """Acheter un billet (route publique)"""
    try:
        data = request.get_json()
        is_valid, errors = validate_ticket_purchase(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        ticket_type = db.ticket_types.find_one({"_id": ObjectId(data['ticket_type_id'])})
        if not ticket_type:
            return not_found_response("Type de billet non trouvé")
        
        if ticket_type['remaining'] <= 0:
            return error_response("Plus de billets disponibles pour ce type", 400)
        
        # Vérifier que l'événement est public
        event = db.events.find_one({"_id": ticket_type['event_id']})
        if event.get('is_private'):
            return error_response("Impossible d'acheter des billets pour un événement privé", 403)
        
        ticket_data = {
            "ticket_type_id": ObjectId(data['ticket_type_id']),
            "ticket_type_name": ticket_type['name'],
            "event_id": ticket_type['event_id'],
            "buyer_first_name": data['buyer_first_name'],
            "buyer_last_name": data['buyer_last_name'],
            "buyer_email": data['buyer_email'],
            "buyer_address": data['buyer_address'],
            "price_paid": ticket_type['price'],
            "purchase_date": datetime.utcnow(),
            "ticket_number": f"T-{ObjectId()}"  # Générer un numéro de billet unique
        }
        
        result = db.tickets.insert_one(ticket_data)
        
        # Décrémenter le nombre de billets restants
        db.ticket_types.update_one(
            {"_id": ObjectId(data['ticket_type_id'])},
            {"$inc": {"remaining": -1}}
        )
        
        ticket = db.tickets.find_one({"_id": result.inserted_id})
        
        return created_response(ticket, "Billet acheté avec succès")
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@tickets_bp.route('/event/<event_id>', methods=['GET'])
@token_required
def get_event_tickets(current_user, event_id):
    """Récupérer les billets vendus pour un événement (organisateurs uniquement)"""
    try:
        if not ObjectId.is_valid(event_id):
            return error_response("ID événement invalide", 400)
        
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return not_found_response("Événement non trouvé")
        
        if ObjectId(current_user['_id']) not in event['organizers']:
            return error_response("Seuls les organisateurs peuvent voir les billets vendus", 403)
        
        tickets = list(db.tickets.find({"event_id": ObjectId(event_id)}).sort("purchase_date", -1))
        
        # Calculer les statistiques
        total_revenue = sum(t.get('price_paid', 0) for t in tickets)
        
        return success_response({
            "tickets": tickets,
            "total_sold": len(tickets),
            "total_revenue": total_revenue
        })
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)

@tickets_bp.route('/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Récupérer un billet par son ID (route publique pour vérification)"""
    try:
        if not ObjectId.is_valid(ticket_id):
            return error_response("ID billet invalide", 400)
        
        db = get_db()
        ticket = db.tickets.find_one({"_id": ObjectId(ticket_id)})
        if not ticket:
            return not_found_response("Billet non trouvé")
        
        # Récupérer les infos de l'événement
        event = db.events.find_one({"_id": ticket['event_id']}, {"name": 1, "start_date": 1, "location": 1})
        
        return success_response({
            "ticket": ticket,
            "event": event
        })
    except Exception as e:
        return error_response(f"Erreur: {str(e)}", 500)