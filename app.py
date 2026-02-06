"""
My Social Networks API
Application principale Flask

Auteur: Salma
Date: Février 2026
Description: API REST pour une plateforme de réseau social avec gestion d'événements,
             groupes, discussions, billetterie, shopping list et covoiturage.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from utils import init_db
import os

def create_app(config_class=Config):
    """
    Factory pour créer l'application Flask
    
    Args:
        config_class: Classe de configuration à utiliser
        
    Returns:
        app: Instance de l'application Flask configurée
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Activer CORS pour permettre les requêtes cross-origin
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialiser la base de données MongoDB
    init_db(app)
    
    # Créer le dossier d'upload s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # ========================================================================
    # Enregistrement des Blueprints (Routes)
    # ========================================================================
    
    # Routes principales
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.events import events_bp
    from routes.groups import groups_bp
    from routes.discussions import discussions_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(discussions_bp)
    
    # Routes pour les fonctionnalités supplémentaires
    try:
        from routes.albums import albums_bp
        app.register_blueprint(albums_bp)
        print("✓ Module Albums chargé")
    except ImportError as e:
        print(f"⚠ Module Albums non chargé: {e}")
    
    try:
        from routes.polls import polls_bp
        app.register_blueprint(polls_bp)
        print("✓ Module Polls chargé")
    except ImportError as e:
        print(f"⚠ Module Polls non chargé: {e}")
    
    try:
        from routes.tickets import tickets_bp
        app.register_blueprint(tickets_bp)
        print("✓ Module Tickets chargé")
    except ImportError as e:
        print(f"⚠ Module Tickets non chargé: {e}")
    
    # Routes BONUS
    try:
        from routes.shopping import shopping_bp
        app.register_blueprint(shopping_bp)
        print("✓ Module Shopping (BONUS) chargé")
    except ImportError as e:
        print(f"⚠ Module Shopping non chargé: {e}")
    
    try:
        from routes.carpooling import carpooling_bp
        app.register_blueprint(carpooling_bp)
        print("✓ Module Carpooling (BONUS) chargé")
    except ImportError as e:
        print(f"⚠ Module Carpooling non chargé: {e}")
    
    # ========================================================================
    # Routes de base
    # ========================================================================
    
    @app.route('/')
    def index():
        """Route d'accueil de l'API"""
        return jsonify({
            "message": "Bienvenue sur l'API My Social Networks",
            "version": "1.0.0",
            "author": "Salma",
            "description": "API REST pour la gestion d'événements, groupes et réseaux sociaux",
            "documentation": "/api/docs",
            "endpoints": {
                "authentication": {
                    "register": "POST /api/auth/register",
                    "login": "POST /api/auth/login",
                    "me": "GET /api/auth/me"
                },
                "users": {
                    "list": "GET /api/users",
                    "get": "GET /api/users/<user_id>",
                    "update": "PUT /api/users/<user_id>",
                    "delete": "DELETE /api/users/<user_id>"
                },
                "events": {
                    "create": "POST /api/events",
                    "list": "GET /api/events",
                    "get": "GET /api/events/<event_id>",
                    "update": "PUT /api/events/<event_id>",
                    "delete": "DELETE /api/events/<event_id>",
                    "join": "POST /api/events/<event_id>/join",
                    "leave": "POST /api/events/<event_id>/leave"
                },
                "groups": {
                    "create": "POST /api/groups",
                    "list": "GET /api/groups",
                    "get": "GET /api/groups/<group_id>",
                    "update": "PUT /api/groups/<group_id>",
                    "join": "POST /api/groups/<group_id>/join",
                    "leave": "POST /api/groups/<group_id>/leave"
                },
                "discussions": {
                    "event_messages": "GET /api/discussions/event/<event_id>/messages",
                    "post_event_message": "POST /api/discussions/event/<event_id>/messages",
                    "group_messages": "GET /api/discussions/group/<group_id>/messages",
                    "post_group_message": "POST /api/discussions/group/<group_id>/messages"
                },
                "albums": {
                    "create": "POST /api/albums",
                    "get_event_albums": "GET /api/albums/event/<event_id>",
                    "add_photo": "POST /api/albums/<album_id>/photos",
                    "get_photos": "GET /api/albums/<album_id>/photos",
                    "comment": "POST /api/albums/photos/<photo_id>/comments"
                },
                "polls": {
                    "create": "POST /api/polls",
                    "get_event_polls": "GET /api/polls/event/<event_id>",
                    "respond": "POST /api/polls/<poll_id>/respond",
                    "results": "GET /api/polls/<poll_id>/results"
                },
                "tickets": {
                    "create_type": "POST /api/tickets/types",
                    "get_types": "GET /api/tickets/types/event/<event_id>",
                    "purchase": "POST /api/tickets/purchase",
                    "get_sold": "GET /api/tickets/event/<event_id>"
                },
                "shopping (BONUS)": {
                    "create": "POST /api/shopping",
                    "get_event_items": "GET /api/shopping/event/<event_id>",
                    "update": "PUT /api/shopping/<item_id>",
                    "delete": "DELETE /api/shopping/<item_id>"
                },
                "carpooling (BONUS)": {
                    "create": "POST /api/carpooling",
                    "get_event_offers": "GET /api/carpooling/event/<event_id>",
                    "update": "PUT /api/carpooling/<offer_id>",
                    "book": "POST /api/carpooling/<offer_id>/book",
                    "cancel": "POST /api/carpooling/<offer_id>/cancel",
                    "delete": "DELETE /api/carpooling/<offer_id>"
                }
            },
            "features": {
                "authentication": "JWT Token-based authentication",
                "events": "Public/Private events with organizers and participants",
                "groups": "Public/Private/Secret groups",
                "discussions": "Message threads for events and groups",
                "albums": "Photo albums with comments",
                "polls": "Surveys with multiple questions",
                "ticketing": "Ticket sales for public events",
                "shopping_list": "BONUS - Items to bring to events",
                "carpooling": "BONUS - Ride sharing for events"
            },
            "status": "operational",
            "github": "https://github.com/votre-repo",
            "contact": "salma@example.com"
        }), 200
    
    @app.route('/api/health')
    def health():
        """Vérification de l'état de l'API"""
        try:
            # Vérifier la connexion à MongoDB
            from utils import get_db
            db = get_db()
            db.command('ping')
            
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "message": "API is running smoothly"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }), 503
    
    @app.route('/api/stats')
    def stats():
        """Statistiques générales de l'API (route publique)"""
        try:
            from utils import get_db
            db = get_db()
            
            return jsonify({
                "statistics": {
                    "users": db.users.count_documents({}),
                    "events": db.events.count_documents({}),
                    "groups": db.groups.count_documents({}),
                    "albums": db.albums.count_documents({}),
                    "photos": db.photos.count_documents({}),
                    "polls": db.polls.count_documents({}),
                    "tickets_sold": db.tickets.count_documents({}),
                    "shopping_items": db.shopping_items.count_documents({}),
                    "carpooling_offers": db.carpooling.count_documents({})
                }
            }), 200
        except Exception as e:
            return jsonify({
                "error": "Could not fetch statistics",
                "message": str(e)
            }), 500
    
    # ========================================================================
    # Gestion des erreurs
    # ========================================================================
    
    @app.errorhandler(404)
    def not_found(error):
        """Gestionnaire d'erreur 404 - Route non trouvée"""
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": "La route demandée n'existe pas",
            "status_code": 404
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Gestionnaire d'erreur 405 - Méthode non autorisée"""
        return jsonify({
            "success": False,
            "error": "Method Not Allowed",
            "message": "La méthode HTTP utilisée n'est pas autorisée pour cette route",
            "status_code": 405
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Gestionnaire d'erreur 500 - Erreur interne du serveur"""
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "Une erreur interne s'est produite sur le serveur",
            "status_code": 500
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Gestionnaire d'erreur 400 - Requête invalide"""
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "La requête est invalide ou mal formée",
            "status_code": 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Gestionnaire d'erreur 401 - Non authentifié"""
        return jsonify({
            "success": False,
            "error": "Unauthorized",
            "message": "Authentification requise",
            "status_code": 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Gestionnaire d'erreur 403 - Accès interdit"""
        return jsonify({
            "success": False,
            "error": "Forbidden",
            "message": "Vous n'avez pas les permissions nécessaires",
            "status_code": 403
        }), 403
    
    # ========================================================================
    # Middleware pour logger les requêtes (optionnel)
    # ========================================================================
    
    @app.before_request
    def log_request():
        """Logger les requêtes entrantes (utile pour le débogage)"""
        if app.config['DEBUG']:
            from flask import request
            print(f"[{request.method}] {request.path}")
    
    @app.after_request
    def after_request(response):
        """Ajouter des headers de sécurité"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    return app


# ============================================================================
# Point d'entrée de l'application
# ============================================================================

if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*70)
    print(" MY SOCIAL NETWORKS API")
    print("="*70)
    print(" Projet: API REST pour réseau social")
    print(" Auteur: Salma")
    print(" Date: Février 2026")
    print("="*70)
    print("\n Fonctionnalités disponibles:")
    print("   -  Authentification JWT")
    print("   -  Gestion des utilisateurs")
    print("   -  Événements (publics/privés)")
    print("   -  Groupes (public/privé/secret)")
    print("   -  Discussions et messages")
    print("   -  Albums photos avec commentaires")
    print("   -  Sondages")
    print("   -  Billetterie")
    print("   -  Shopping list (BONUS)")
    print("   -  Covoiturage (BONUS)")
    print("\n" + "="*70)
    print(f" Serveur: http://localhost:{app.config.get('PORT', 5000)}")
    print(f" Mode: {'DEBUG' if app.config['DEBUG'] else 'PRODUCTION'}")
    print(f" MongoDB: {app.config['MONGO_URI'].split('@')[-1] if '@' in app.config['MONGO_URI'] else app.config['MONGO_URI']}")
    print("="*70 + "\n")
    
    # Démarrer le serveur
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=port,
        threaded=True
    )