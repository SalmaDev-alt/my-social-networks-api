"""
Modèle Event - Structure d'un événement dans MongoDB

Collection: events
"""

from datetime import datetime
from bson import ObjectId

class EventModel:
    """
    Représente un événement sur la plateforme
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document événement
        """
        return {
            "_id": ObjectId(),
            "name": str,  # Requis
            "description": str,  # Requis
            "start_date": datetime,  # Requis
            "end_date": datetime,  # Requis
            "location": str,  # Requis
            "cover_photo": str,  # URL, optionnel
            "is_private": bool,  # Défaut: False
            "organizers": [ObjectId()],  # Liste d'IDs utilisateurs, au moins 1
            "participants": [ObjectId()],  # Liste d'IDs utilisateurs
            "group_id": ObjectId(),  # Optionnel, si créé depuis un groupe
            "has_ticketing": bool,  # Défaut: False
            "has_shopping_list": bool,  # Défaut: False (BONUS)
            "has_carpooling": bool,  # Défaut: False (BONUS)
            "created_at": datetime,
            "updated_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document événement
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439012"),
            "name": "Anniversaire de Marie",
            "description": "Soirée d'anniversaire pour célébrer les 30 ans de Marie",
            "start_date": datetime(2026, 3, 15, 19, 0),
            "end_date": datetime(2026, 3, 16, 2, 0),
            "location": "123 Avenue des Champs-Élysées, Paris",
            "cover_photo": "https://example.com/events/marie-30.jpg",
            "is_private": True,
            "organizers": [
                ObjectId("507f1f77bcf86cd799439011"),
                ObjectId("507f1f77bcf86cd799439013")
            ],
            "participants": [
                ObjectId("507f1f77bcf86cd799439011"),
                ObjectId("507f1f77bcf86cd799439013"),
                ObjectId("507f1f77bcf86cd799439014")
            ],
            "group_id": ObjectId("507f1f77bcf86cd799439020"),
            "has_ticketing": False,
            "has_shopping_list": True,
            "has_carpooling": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection events
        """
        return [
            {"key": "start_date"},
            {"key": "is_private"},
            {"key": "organizers"},
            {"key": "participants"},
            {"key": "group_id"},
            {"key": "created_at"}
        ]