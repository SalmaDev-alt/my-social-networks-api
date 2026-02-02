from functools import wraps
from flask import request
import jwt
from bson import ObjectId
from config import Config
from utils import get_db, unauthorized_response, error_response

def token_required(f):
    """Décorateur pour protéger les routes avec JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Récupérer le token depuis le header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Format: "Bearer TOKEN"
            except IndexError:
                return unauthorized_response("Format de token invalide. Utilisez: Bearer <token>")
        
        if not token:
            return unauthorized_response("Token d'authentification manquant")
        
        try:
            # Décoder le token
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            
            # Récupérer l'utilisateur depuis la base de données
            db = get_db()
            current_user = db.users.find_one({"_id": ObjectId(data['user_id'])})
            
            if not current_user:
                return unauthorized_response("Utilisateur non trouvé")
            
        except jwt.ExpiredSignatureError:
            return unauthorized_response("Token expiré")
        except jwt.InvalidTokenError:
            return unauthorized_response("Token invalide")
        except Exception as e:
            return error_response(f"Erreur d'authentification: {str(e)}", 401)
        
        # Passer l'utilisateur à la fonction décorée
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated

def optional_token(f):
    """Décorateur pour les routes qui acceptent mais ne requièrent pas un token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
                data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
                db = get_db()
                current_user = db.users.find_one({"_id": ObjectId(data['user_id'])})
            except:
                pass
        
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated