"""
Modèle ShoppingItem - Structure d'un item de shopping list dans MongoDB

Collection: shopping_items
"""

from datetime import datetime
from bson import ObjectId

class ShoppingItemModel:
    """
    Représente un item à apporter à un événement (BONUS)
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document shopping item
        """
        return {
            "_id": ObjectId(),
            "name": str,  # Requis, unique par événement
            "quantity": int,  # Requis, >= 1
            "arrival_time": datetime,  # Heure d'arrivée prévue
            "event_id": ObjectId(),  # Requis
            "user_id": ObjectId(),  # Utilisateur qui apporte l'item
            "user_name": str,  # Nom complet de l'utilisateur
            "notes": str,  # Notes additionnelles, optionnel
            "created_at": datetime,
            "updated_at": datetime  # Optionnel
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document shopping item
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439070"),
            "name": "Chips",
            "quantity": 3,
            "arrival_time": datetime(2026, 3, 15, 19, 30),
            "event_id": ObjectId("507f1f77bcf86cd799439012"),
            "user_id": ObjectId("507f1f77bcf86cd799439011"),
            "user_name": "John Doe",
            "notes": "Format familial, saveur nature",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection shopping_items
        """
        return [
            {"key": "event_id"},
            {"key": "user_id"},
            {"key": [("event_id", 1), ("name", 1)], "unique": True},  # Unicité par événement
            {"key": "arrival_time"}
        ]