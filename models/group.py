"""
Modèle Group - Structure d'un groupe dans MongoDB

Collection: groups
"""

from datetime import datetime
from bson import ObjectId

class GroupModel:
    """
    Représente un groupe sur la plateforme
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document groupe
        """
        return {
            "_id": ObjectId(),
            "name": str,  # Requis
            "description": str,  # Requis
            "icon": str,  # URL, optionnel
            "cover_photo": str,  # URL, optionnel
            "group_type": str,  # "public", "private", ou "secret", requis
            "allow_members_to_post": bool,  # Défaut: True
            "allow_members_to_create_events": bool,  # Défaut: True
            "administrators": [ObjectId()],  # Liste d'IDs utilisateurs, au moins 1
            "members": [ObjectId()],  # Liste d'IDs utilisateurs
            "created_at": datetime,
            "updated_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document groupe
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439020"),
            "name": "Amis de l'université",
            "description": "Groupe pour les anciens de la Promo 2020",
            "icon": "https://example.com/groups/icons/univ.png",
            "cover_photo": "https://example.com/groups/covers/univ.jpg",
            "group_type": "private",
            "allow_members_to_post": True,
            "allow_members_to_create_events": True,
            "administrators": [
                ObjectId("507f1f77bcf86cd799439011")
            ],
            "members": [
                ObjectId("507f1f77bcf86cd799439011"),
                ObjectId("507f1f77bcf86cd799439013"),
                ObjectId("507f1f77bcf86cd799439014"),
                ObjectId("507f1f77bcf86cd799439015")
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection groups
        """
        return [
            {"key": "group_type"},
            {"key": "administrators"},
            {"key": "members"},
            {"key": "created_at"}
        ]