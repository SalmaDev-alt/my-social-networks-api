import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de l'application"""
    
    # Configuration Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'votre_secret_key_super_securisee_a_changer')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Configuration MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/my_social_networks')
    
    # Configuration JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key_super_securisee_a_changer')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Configuration de l'upload de fichiers
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Configuration CORS
    CORS_HEADERS = 'Content-Type'