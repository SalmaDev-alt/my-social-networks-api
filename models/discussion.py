"""
Modèle Discussion - Structure d'une discussion dans MongoDB

Collection: discussions
"""

from datetime import datetime
from bson import ObjectId

class DiscussionModel:
    """
    Représente un fil de discussion (pour un événement OU un groupe)
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document discussion
        """
        return {
            "_id": ObjectId(),
            "event_id": ObjectId(),  # Soit event_id, soit group_id (pas les deux)
            "group_id": ObjectId(),  # Soit event_id, soit group_id (pas les deux)
            "messages": [
                {
                    "_id": ObjectId(),
                    "author_id": ObjectId(),
                    "author_name": str,
                    "content": str,
                    "parent_message_id": ObjectId(),  # Pour les réponses, optionnel
                    "created_at": datetime
                }
            ],
            "created_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document discussion
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439030"),
            "event_id": ObjectId("507f1f77bcf86cd799439012"),
            "group_id": None,
            "messages": [
                {
                    "_id": ObjectId("507f1f77bcf86cd799439031"),
                    "author_id": ObjectId("507f1f77bcf86cd799439011"),
                    "author_name": "John Doe",
                    "content": "Salut tout le monde ! J'ai hâte d'être à samedi !",
                    "parent_message_id": None,
                    "created_at": datetime.utcnow()
                },
                {
                    "_id": ObjectId("507f1f77bcf86cd799439032"),
                    "author_id": ObjectId("507f1f77bcf86cd799439013"),
                    "author_name": "Jane Smith",
                    "content": "Moi aussi ! Ça va être génial !",
                    "parent_message_id": ObjectId("507f1f77bcf86cd799439031"),
                    "created_at": datetime.utcnow()
                }
            ],
            "created_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection discussions
        """
        return [
            {"key": "event_id"},
            {"key": "group_id"},
            {"key": "created_at"}
        ]