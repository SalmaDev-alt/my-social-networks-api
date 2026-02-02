"""
Modèle Message - Structure d'un message dans une discussion

Note: Les messages sont stockés comme sous-documents dans les discussions,
mais ce modèle documente leur structure.
"""

from datetime import datetime
from bson import ObjectId

class MessageModel:
    """
    Représente un message dans un fil de discussion
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un message
        """
        return {
            "_id": ObjectId(),
            "author_id": ObjectId(),  # Requis
            "author_name": str,  # Nom complet de l'auteur
            "content": str,  # Requis, max 5000 caractères
            "parent_message_id": ObjectId(),  # Optionnel, pour les réponses
            "created_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un message
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439031"),
            "author_id": ObjectId("507f1f77bcf86cd799439011"),
            "author_name": "John Doe",
            "content": "Salut tout le monde ! J'ai hâte d'être à samedi !",
            "parent_message_id": None,
            "created_at": datetime.utcnow()
        }