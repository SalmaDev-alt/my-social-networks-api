"""
Modèle Ticket - Structure des billets et types de billets dans MongoDB

Collections: tickets, ticket_types
"""

from datetime import datetime
from bson import ObjectId

class TicketTypeModel:
    """
    Représente un type de billet créé par un organisateur
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document type de billet
        """
        return {
            "_id": ObjectId(),
            "name": str,  # Requis (ex: "Billet Standard")
            "price": float,  # Requis, >= 0
            "quantity": int,  # Requis, nombre total de billets
            "remaining": int,  # Nombre de billets restants
            "description": str,  # Optionnel
            "event_id": ObjectId(),  # Requis
            "created_by": ObjectId(),  # ID de l'organisateur
            "created_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document type de billet
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439060"),
            "name": "Billet Standard",
            "price": 25.00,
            "quantity": 100,
            "remaining": 87,
            "description": "Accès standard à l'événement",
            "event_id": ObjectId("507f1f77bcf86cd799439012"),
            "created_by": ObjectId("507f1f77bcf86cd799439011"),
            "created_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection ticket_types
        """
        return [
            {"key": "event_id"},
            {"key": "created_at"}
        ]


class TicketModel:
    """
    Représente un billet acheté par une personne
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document billet
        """
        return {
            "_id": ObjectId(),
            "ticket_type_id": ObjectId(),  # Requis
            "ticket_type_name": str,  # Nom du type de billet
            "event_id": ObjectId(),  # Requis
            "buyer_first_name": str,  # Requis
            "buyer_last_name": str,  # Requis
            "buyer_email": str,  # Requis
            "buyer_address": {
                "street": str,
                "city": str,
                "postal_code": str,
                "country": str
            },  # Requis
            "price_paid": float,  # Prix payé
            "purchase_date": datetime,  # Date d'achat
            "ticket_number": str  # Numéro unique du billet
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document billet
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439061"),
            "ticket_type_id": ObjectId("507f1f77bcf86cd799439060"),
            "ticket_type_name": "Billet Standard",
            "event_id": ObjectId("507f1f77bcf86cd799439012"),
            "buyer_first_name": "Marie",
            "buyer_last_name": "Dupont",
            "buyer_email": "marie.dupont@example.com",
            "buyer_address": {
                "street": "45 Rue de la République",
                "city": "Lyon",
                "postal_code": "69001",
                "country": "France"
            },
            "price_paid": 25.00,
            "purchase_date": datetime.utcnow(),
            "ticket_number": "T-507f1f77bcf86cd799439061"
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection tickets
        """
        return [
            {"key": "ticket_type_id"},
            {"key": "event_id"},
            {"key": "buyer_email"},
            {"key": "ticket_number", "unique": True},
            {"key": "purchase_date"}
        ]