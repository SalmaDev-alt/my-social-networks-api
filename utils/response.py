from flask import jsonify
from bson import ObjectId
from datetime import datetime

def serialize_doc(doc):
    """Convertit un document MongoDB en format JSON"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, dict):
                serialized[key] = serialize_doc(value)
            elif isinstance(value, list):
                serialized[key] = [serialize_doc(item) if isinstance(item, (dict, ObjectId)) else item for item in value]
            else:
                serialized[key] = value
        return serialized
    
    if isinstance(doc, ObjectId):
        return str(doc)
    
    return doc

def success_response(data=None, message="Success", status=200):
    """Retourne une réponse de succès standardisée"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = serialize_doc(data)
    
    return jsonify(response), status

def error_response(message="Error", status=400, errors=None):
    """Retourne une réponse d'erreur standardisée"""
    response = {
        "success": False,
        "message": message
    }
    if errors:
        response["errors"] = errors
    
    return jsonify(response), status

def created_response(data, message="Created successfully"):
    """Retourne une réponse de création réussie"""
    return success_response(data, message, 201)

def not_found_response(message="Resource not found"):
    """Retourne une réponse 404"""
    return error_response(message, 404)

def unauthorized_response(message="Unauthorized"):
    """Retourne une réponse 401"""
    return error_response(message, 401)

def forbidden_response(message="Forbidden"):
    """Retourne une réponse 403"""
    return error_response(message, 403)