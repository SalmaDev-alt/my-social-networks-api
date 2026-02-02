"""
Modèle Carpooling - Structure d'une offre de covoiturage dans MongoDB

Collection: carpooling
"""

from datetime import datetime
from bson import ObjectId

class CarpoolingModel:
    """
    Représente une offre de covoiturage pour un événement (BONUS)
    """
    
    @staticmethod
    def schema():
        """
        Retourne la structure d'un document covoiturage
        """
        return {
            "_id": ObjectId(),
            "departure_location": str,  # Requis
            "departure_time": datetime,  # Requis
            "price": float,  # Requis, >= 0
            "available_seats": int,  # Places disponibles actuelles
            "total_seats": int,  # Total de places au départ
            "max_time_difference": int,  # En minutes, écart max accepté
            "event_id": ObjectId(),  # Requis
            "driver_id": ObjectId(),  # ID du conducteur
            "driver_name": str,  # Nom complet du conducteur
            "passengers": [
                {
                    "user_id": ObjectId(),
                    "user_name": str,
                    "seats_booked": int,
                    "booked_at": datetime
                }
            ],
            "notes": str,  # Notes additionnelles, optionnel
            "created_at": datetime,
            "updated_at": datetime  # Optionnel
        }
    
    @staticmethod
    def example():
        """
        Exemple d'un document covoiturage
        """
        return {
            "_id": ObjectId("507f1f77bcf86cd799439080"),
            "departure_location": "Gare de Lyon, Paris",
            "departure_time": datetime(2026, 3, 15, 17, 0),
            "price": 10.00,
            "available_seats": 1,
            "total_seats": 3,
            "max_time_difference": 30,
            "event_id": ObjectId("507f1f77bcf86cd799439012"),
            "driver_id": ObjectId("507f1f77bcf86cd799439011"),
            "driver_name": "John Doe",
            "passengers": [
                {
                    "user_id": ObjectId("507f1f77bcf86cd799439013"),
                    "user_name": "Jane Smith",
                    "seats_booked": 1,
                    "booked_at": datetime.utcnow()
                },
                {
                    "user_id": ObjectId("507f1f77bcf86cd799439014"),
                    "user_name": "Bob Martin",
                    "seats_booked": 1,
                    "booked_at": datetime.utcnow()
                }
            ],
            "notes": "Musique autorisée, pas de fumée",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    @staticmethod
    def indexes():
        """
        Index recommandés pour la collection carpooling
        """
        return [
            {"key": "event_id"},
            {"key": "driver_id"},
            {"key": "departure_time"},
            {"key": "available_seats"}
        ]