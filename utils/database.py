from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

def init_db(app):
    """Initialise la connexion à la base de données"""
    mongo.init_app(app)
    return mongo

def get_db():
    """Retourne la base de données"""
    return mongo.db

class PyObjectId(ObjectId):
    """Classe pour gérer les ObjectId de MongoDB"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")