from flask import Blueprint, request
from bson import ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from config import Config
from utils import get_db, success_response, error_response, created_response
from validators import validate_user_registration, validate_user_login

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    try:
        data = request.get_json()
        
        # Validation des données
        is_valid, errors = validate_user_registration(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        
        # Vérifier si l'email existe déjà
        if db.users.find_one({"email": data['email']}):
            return error_response("Un utilisateur avec cet email existe déjà", 400)
        
        # Hasher le mot de passe
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Créer l'utilisateur
        user_data = {
            "email": data['email'],
            "password": hashed_password,
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "phone": data.get('phone'),
            "birth_date": data.get('birth_date'),
            "address": data.get('address'),
            "bio": data.get('bio'),
            "profile_picture": data.get('profile_picture'),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db.users.insert_one(user_data)
        
        # Générer le token JWT
        token = jwt.encode({
            'user_id': str(result.inserted_id),
            'email': data['email'],
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }, Config.JWT_SECRET_KEY, algorithm="HS256")
        
        # Récupérer l'utilisateur créé
        user = db.users.find_one({"_id": result.inserted_id})
        user.pop('password')  # Ne pas retourner le mot de passe
        
        return created_response({
            "user": user,
            "token": token
        }, "Utilisateur créé avec succès")
        
    except Exception as e:
        return error_response(f"Erreur lors de l'inscription: {str(e)}", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Connexion d'un utilisateur"""
    try:
        data = request.get_json()
        
        # Validation des données
        is_valid, errors = validate_user_login(data)
        if not is_valid:
            return error_response("Données invalides", 400, errors)
        
        db = get_db()
        
        # Récupérer l'utilisateur
        user = db.users.find_one({"email": data['email']})
        
        if not user:
            return error_response("Email ou mot de passe incorrect", 401)
        
        # Vérifier le mot de passe
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            return error_response("Email ou mot de passe incorrect", 401)
        
        # Générer le token JWT
        token = jwt.encode({
            'user_id': str(user['_id']),
            'email': user['email'],
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }, Config.JWT_SECRET_KEY, algorithm="HS256")
        
        # Retirer le mot de passe
        user.pop('password')
        
        return success_response({
            "user": user,
            "token": token
        }, "Connexion réussie")
        
    except Exception as e:
        return error_response(f"Erreur lors de la connexion: {str(e)}", 500)

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Récupérer les informations de l'utilisateur connecté"""
    from middleware import token_required
    
    @token_required
    def get_user(current_user):
        # Retirer le mot de passe
        current_user.pop('password', None)
        return success_response(current_user, "Utilisateur récupéré")
    
    return get_user()