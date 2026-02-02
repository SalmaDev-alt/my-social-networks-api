"""
Modèle Photo - Structure d'une photo dans MongoDB

Collection: photos
"""

from datetime import datetime
from bson import ObjectId

class PhotoModel:
    """
    Représente une photo dans un album
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document photo
        """
        return {
            "_id": ObjectId(),
            "url": str,  # URL de la photo, requis
            "caption": str,  # Légende, optionnel
            "album_id": ObjectId(),  # Requis
            "posted_by": ObjectId(),  # ID de l'utilisateur, requis
            "posted_by_name": str,  # Nom complet
            "comments": [
                {
                    "_id": ObjectId(),
                    "author_id": ObjectId(),
                    "author_name": str,
                    "content": str,
                    "created_at": datetime
                }
            ],
            "created_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document photo
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439041"),
            "url": "https://example.com/photos/birthday-cake.jpg",
            "caption": "Le magnifique gâteau d'anniversaire !",
            "album_id": ObjectId("507f1f77bcf86cd799439040"),
            "posted_by": ObjectId("507f1f77bcf86cd799439011"),
            "posted_by_name": "John Doe",
            "comments": [
                {
                    "_id": ObjectId("507f1f77bcf86cd799439042"),
                    "author_id": ObjectId("507f1f77bcf86cd799439013"),
                    "author_name": "Jane Smith",
                    "content": "Wow, il a l'air délicieux ! 🎂",
                    "created_at": datetime.utcnow()
                }
            ],
            "created_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection photos
        """
        return [
            {"key": "album_id"},
            {"key": "posted_by"},
            {"key": "created_at"}
        ]