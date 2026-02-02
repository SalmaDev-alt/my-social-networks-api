"""
Modèle Poll - Structure d'un sondage dans MongoDB

Collection: polls
"""

from datetime import datetime
from bson import ObjectId

class PollModel:
    """
    Représente un sondage pour un événement
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document sondage
        """
        return {
            "_id": ObjectId(),
            "title": str,  # Requis
            "description": str,  # Optionnel
            "event_id": ObjectId(),  # Requis
            "questions": [
                {
                    "question": str,  # Texte de la question
                    "options": [str]  # Liste d'options (minimum 2)
                }
            ],
            "allow_multiple_votes": bool,  # Défaut: False
            "responses": [
                {
                    "user_id": ObjectId(),
                    "user_name": str,
                    "responses": [
                        {
                            "question_index": int,
                            "option_index": int
                        }
                    ],
                    "created_at": datetime
                }
            ],
            "created_by": ObjectId(),
            "created_at": datetime
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document sondage
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439050"),
            "title": "Choix du menu",
            "description": "Votez pour votre menu préféré pour la soirée",
            "event_id": ObjectId("507f1f77bcf86cd799439012"),
            "questions": [
                {
                    "question": "Quel type de cuisine préférez-vous ?",
                    "options": ["Italienne", "Japonaise", "Française", "Mexicaine"]
                },
                {
                    "question": "Préférence de dessert ?",
                    "options": ["Tiramisu", "Tarte tatin", "Cheesecake"]
                }
            ],
            "allow_multiple_votes": False,
            "responses": [
                {
                    "user_id": ObjectId("507f1f77bcf86cd799439011"),
                    "user_name": "John Doe",
                    "responses": [
                        {"question_index": 0, "option_index": 1},
                        {"question_index": 1, "option_index": 0}
                    ],
                    "created_at": datetime.utcnow()
                }
            ],
            "created_by": ObjectId("507f1f77bcf86cd799439011"),
            "created_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection polls
        """
        return [
            {"key": "event_id"},
            {"key": "created_by"},
            {"key": "created_at"}
        ]