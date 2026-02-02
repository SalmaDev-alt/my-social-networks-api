"""
Modèle User - Structure d'un utilisateur dans MongoDB

Collection: users
"""

from datetime import datetime
from bson import ObjectId

class UserModel:
    """
    Représente un utilisateur de la plateforme
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document utilisateur
        """
        return {
            "_id": ObjectId(),
            "email": str,  # Unique, requis
            "password": str,  # Hashé avec bcrypt, requis
            "first_name": str,  # Requis
            "last_name": str,  # Requis
            "phone": str,  # Optionnel
            "birth_date": datetime,  # Optionnel
            "address": {
                "street": str,
                "city": str,
                "postal_code": str,
                "country": str
            },  # Optionnel
            "bio": str,  # Optionnel, max 500 caractères
            "profile_picture": str,  # URL, optionnel
            "created_at": datetime,  # Date de création du compte
            "updated_at": datetime  # Date de dernière modification
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document utilisateur
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "email": "john.doe@example.com",
            "password": "$2b$12$KIXx.xGwI8jE5l4ZYvL8V.YlzV8BxQmZLvQ8H1KmZwvQV8XvL8V",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+33612345678",
            "birth_date": datetime(1990, 1, 15),
            "address": {
                "street": "123 Rue de la Paix",
                "city": "Paris",
                "postal_code": "75001",
                "country": "France"
            },
            "bio": "Passionné de technologie et d'événements",
            "profile_picture": "https://example.com/profiles/john.jpg",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection users
        """
        return [
            {"key": "email", "unique": True},
            {"key": "created_at"}
        ]