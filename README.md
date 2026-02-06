# My Social Networks API 

**Auteur :** Salma DISSI 
**Formation :** Mastère Data Engineering & AI (EFREI Paris)  
**Date :** Février 2026  
**Projet :** API REST pour réseau social avec gestion d'événements et groupes

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)](https://www.mongodb.com/)

---

## Description

API REST complète pour la gestion d'événements, de groupes et de réseaux sociaux développée avec Flask et MongoDB.

### Fonctionnalités

#### Principales
-  **Authentification** - JWT Token-based
-  **Utilisateurs** - CRUD complet avec profils
-  **Événements** - Publics/Privés avec organisateurs et participants
-  **Groupes** - Public/Privé/Secret avec système de permissions
-  **Discussions** - Fils de messages pour événements et groupes
-  **Albums photos** - Avec système de commentaires
-  **Sondages** - Questions multiples pour événements
-  **Billetterie** - Vente de billets pour événements publics

#### BONUS 
-  **Shopping List** - Items à apporter aux événements (uniques par événement)
-  **Covoiturage** - Offres de covoiturage avec réservation de places

---

## 🛠 Technologies

- **Backend** : Python 3.11, Flask 3.0.0
- **Base de données** : MongoDB (Atlas/Local)
- **Authentification** : JWT (PyJWT 2.9.0)
- **Validation** : Marshmallow 3.20.1
- **Sécurité** : bcrypt 4.1.2, flask-cors 4.0.0

---

##  Installation

### Prérequis
- Python 3.8+
- MongoDB (local ou MongoDB Atlas)

### Installation rapide
```bash
# Cloner le repository
git clone https://github.com/SalmaDev-alt/my-social-networks-api.git
cd my-social-networks-api

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
copy .env.example .env
# Puis modifier .env avec vos paramètres MongoDB

# Lancer l'application
python app.py
```

L'API sera accessible sur `http://localhost:5000`

---


##  Endpoints principaux

Lien Documentation Postman : https://documenter.getpostman.com/view/44390291/2sBXc8p3yR#cc25a382-ef3c-4001-b668-5db2a4321e7f

### Authentification
```
POST   /api/auth/register        # Inscription
POST   /api/auth/login           # Connexion
GET    /api/auth/me              # Profil utilisateur
```

### Événements
```
POST   /api/events               # Créer un événement
GET    /api/events               # Liste des événements
GET    /api/events/<id>          # Détails d'un événement
POST   /api/events/<id>/join     # Rejoindre un événement
```

### Groupes
```
POST   /api/groups               # Créer un groupe
GET    /api/groups               # Liste des groupes
POST   /api/groups/<id>/join     # Rejoindre un groupe
```

### Shopping List (BONUS)
```
POST   /api/shopping             # Ajouter un item
GET    /api/shopping/event/<id>  # Liste des items
```

### Covoiturage (BONUS)
```
POST   /api/carpooling           # Créer une offre
POST   /api/carpooling/<id>/book # Réserver une place
```

Voir la documentation complète dans `docs/api_documentation.md`

---

##  Tests et Validation

### Collection Postman

Tous les endpoints ont été testés avec Postman. La collection complète est disponible en ligne :

** [Voir la collection Postman](https://web.postman.co/workspace/My-Workspace~652b25ac-3c25-4b97-8738-a34692fe8f1f/collection/44390291-58b0d663-092c-43d0-a6ca-523114be6f24?action=share\&source=copy-link\&creator=44390291)**

** Documentation des tests :** [postman/README.md](postman/README.md)

### Résultats des tests

| Catégorie | Endpoints | Statut |
|-----------|-----------|--------|
| Authentification | 3  |
| Utilisateurs | 2  |
| Événements | 7 | 
| Groupes | 6 | 
| Discussions | 2 | 
| Sondages | 1 | 
| Shopping (BONUS) | 1 | 
| Covoiturage (BONUS) | 1 | 
| Statistiques | 1 | 

**Total : 24+ endpoints testés avec succès **

---

##  Structure du projet
```
my_social_networks_api/
├── app.py                      # Point d'entrée
├── config.py                   # Configuration
├── requirements.txt            # Dépendances
├── .env.example               # Template configuration
│
├── routes/                    # Endpoints API
│   ├── auth.py               # Authentification
│   ├── events.py             # Événements
│   ├── groups.py             # Groupes
│   ├── shopping.py           # Shopping list (BONUS)
│   └── carpooling.py         # Covoiturage (BONUS)
│
├── validators/               # Validation Marshmallow
├── middleware/               # Authentification JWT
├── utils/                    # Utilitaires (DB, réponses)
└── docs/                     # Documentation
```

---

##  Tests

L'API a été entièrement testée avec **Postman**. Tous les endpoints fonctionnent correctement.

### Test rapide
```bash
# Vérifier l'état de l'API
curl http://localhost:5000/api/health

# S'inscrire
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'
```

---

##  Sécurité

-  Authentification JWT obligatoire
-  Hashage des mots de passe avec bcrypt
-  Validation stricte avec Marshmallow
-  CORS configuré
-  Headers de sécurité

---

##  Auteur

**Salma DISSI**  
Étudiante en Mastère Data Engineering & AI (EFREI Paris)

---

##  Licence

Projet académique - Février 2026