"""
Modèle Album - Structure d'un album photo dans MongoDB

Collection: albums
"""

from datetime import datetime
from bson import ObjectId

class AlbumModel:
    """
    Représente un album photo associé à un événement
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document album
        """
        return {
            "_id": ObjectId(),
            "name": str,  # Requis
            "description": str,  # Optionnel
            "event_id": ObjectId(),  # Requis, 1 album = 1 événement
            "created_by": ObjectId(),  # ID de l'utilisateur créateur
            "created_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document album
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439040"),
            "name": "Photos de la soirée",
            "description": "Les meilleurs moments de la soirée d'anniversaire",
            "event_id": ObjectId("507f1f77bcf86cd799439012"),
            "created_by": ObjectId("507f1f77bcf86cd799439011"),
            "created_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection albums
        """
        return [
            {"key": "event_id"},
            {"key": "created_by"},
            {"key": "created_at"}
        ]