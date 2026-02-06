# Documentation API - My Social Networks

## Table des matières

- [Introduction](#introduction)
- [Authentification](#authentification)
- [Formats de réponse](#formats-de-réponse)
- [Codes d'erreur](#codes-derreur)
- [Endpoints](#endpoints)
  - [Authentification](#1-authentification)
  - [Utilisateurs](#2-utilisateurs)
  - [Événements](#3-événements)
  - [Groupes](#4-groupes)
  - [Discussions](#5-discussions)
  - [Albums et Photos](#6-albums-et-photos)
  - [Sondages](#7-sondages)
  - [Billetterie](#8-billetterie)
  - [Shopping List (BONUS)](#9-shopping-list-bonus)
  - [Covoiturage (BONUS)](#10-covoiturage-bonus)
- [Exemples d'utilisation](#exemples-dutilisation)
- [Bonnes pratiques](#bonnes-pratiques)

---

## Introduction

**My Social Networks API** est une API REST complète pour la gestion d'événements, de groupes et de réseaux sociaux.


### Informations générales

- **Base URL**: `http://localhost:5000`
- **Version**: 1.0.0
- **Format**: JSON
- **Authentification**: JWT (JSON Web Token)
- **Auteur**: Salma DISSI
- **Date**: Février 2026
- **GitHub**:  https://github.com/SalmaDev-alt/my-social-networks-api

### Fonctionnalités principales

**Authentification** - Inscription et connexion sécurisées avec JWT  
**Utilisateurs** - Gestion complète des profils utilisateurs  
**Événements** - Événements publics/privés avec organisateurs et participants  
**Groupes** - Groupes publics, privés ou secrets  
**Discussions** - Fils de messages pour événements et groupes  
**Albums** - Albums photos avec système de commentaires  
**Sondages** - Sondages avec questions multiples  
**Billetterie** - Vente de billets pour événements publics  
**Shopping List** - Liste d'items à apporter (BONUS)  
**Covoiturage** - Offres de covoiturage (BONUS)

---

## Authentification

La plupart des endpoints nécessitent un token JWT d'authentification.

### Obtenir un token

1. **S'inscrire** via `POST /api/auth/register`
2. **Se connecter** via `POST /api/auth/login`
3. **Utiliser le token** retourné dans le header `Authorization`

### Format du header
```http
Authorization: Bearer <votre_token_jwt>
```

### Exemple
```bash
curl -X GET http://localhost:5000/api/users \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Formats de réponse

### Réponse de succès
```json
{
  "success": true,
  "message": "Opération réussie",
  "data": {
    // Données demandées
  }
}
```

### Réponse d'erreur
```json
{
  "success": false,
  "message": "Description de l'erreur",
  "errors": {
    // Détails des erreurs de validation (optionnel)
  }
}
```

### Réponse avec pagination
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

---

## Codes d'erreur

| Code | Signification | Description |
|------|---------------|-------------|
| 200 | OK | Requête réussie |
| 201 | Created | Ressource créée avec succès |
| 400 | Bad Request | Requête invalide ou mal formée |
| 401 | Unauthorized | Authentification requise ou token invalide |
| 403 | Forbidden | Accès interdit (permissions insuffisantes) |
| 404 | Not Found | Ressource non trouvée |
| 405 | Method Not Allowed | Méthode HTTP non autorisée |
| 500 | Internal Server Error | Erreur interne du serveur |

---

## Endpoints

## 1. Authentification

### POST `/api/auth/register`

Inscription d'un nouvel utilisateur.

**Authentification requise**:  Non

**Corps de la requête**:
```json
{
  "email": "john.doe@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+33612345678",
  "birth_date": "1990-01-15",
  "bio": "Passionné de technologie",
  "address": {
    "street": "123 Rue de la Paix",
    "city": "Paris",
    "postal_code": "75001",
    "country": "France"
  },
  "profile_picture": "https://example.com/photo.jpg"
}
```

**Champs requis**: `email`, `password`, `first_name`, `last_name`

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Utilisateur créé avec succès",
  "data": {
    "user": {
      "_id": "507f1f77bcf86cd799439011",
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2026-02-01T10:00:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

### POST `/api/auth/login`

Connexion d'un utilisateur existant.

**Authentification requise**:  Non

**Corps de la requête**:
```json
{
  "email": "john.doe@example.com",
  "password": "password123"
}
```

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "user": {
      "_id": "507f1f77bcf86cd799439011",
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

### GET `/api/auth/me`

Récupérer les informations de l'utilisateur connecté.

**Authentification requise**:  Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Utilisateur récupéré",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+33612345678",
    "bio": "Passionné de technologie",
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

## 2. Utilisateurs

### GET `/api/users`

Récupérer la liste des utilisateurs avec pagination et recherche.

**Authentification requise**:  Oui

**Paramètres de requête**:

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| page | integer | 1 | Numéro de la page |
| per_page | integer | 20 | Nombre d'items par page |
| search | string | - | Recherche par nom, prénom ou email |

**Exemple**:
```
GET /api/users?page=1&per_page=10&search=john
```

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "users": [
      {
        "_id": "507f1f77bcf86cd799439011",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

---

### GET `/api/users/<user_id>`

Récupérer les détails d'un utilisateur spécifique.

**Authentification requise**: Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+33612345678",
    "bio": "Passionné de technologie",
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### PUT `/api/users/<user_id>`

Mettre à jour son profil utilisateur.

**Authentification requise**: Oui  
**Restriction**: Vous ne pouvez modifier que votre propre profil

**Corps de la requête**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+33698765432",
  "bio": "Nouvelle bio mise à jour",
  "address": {
    "street": "456 Avenue Nouvelle",
    "city": "Lyon",
    "postal_code": "69001",
    "country": "France"
  }
}
```

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Utilisateur mis à jour avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+33698765432",
    "bio": "Nouvelle bio mise à jour",
    "updated_at": "2026-02-02T14:30:00Z"
  }
}
```

---

### DELETE `/api/users/<user_id>`

Supprimer son compte utilisateur.

**Authentification requise**: Oui  
**Restriction**: Vous ne pouvez supprimer que votre propre compte

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Utilisateur supprimé avec succès",
  "data": null
}
```

---

## 3. Événements

### POST `/api/events`

Créer un nouvel événement.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "name": "Soirée jeux de société",
  "description": "Une soirée sympa entre amis pour jouer",
  "start_date": "2026-04-15T19:00:00Z",
  "end_date": "2026-04-15T23:00:00Z",
  "location": "123 Rue de la Paix, Paris",
  "cover_photo": "https://example.com/event-cover.jpg",
  "is_private": false,
  "group_id": "507f1f77bcf86cd799439020",
  "has_ticketing": false,
  "has_shopping_list": true,
  "has_carpooling": true,
  "organizers": ["507f1f77bcf86cd799439013"],
  "participants": ["507f1f77bcf86cd799439014"]
}
```

**Champs requis**: `name`, `description`, `start_date`, `end_date`, `location`

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Événement créé avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439012",
    "name": "Soirée jeux de société",
    "description": "Une soirée sympa entre amis pour jouer",
    "start_date": "2026-04-15T19:00:00Z",
    "end_date": "2026-04-15T23:00:00Z",
    "location": "123 Rue de la Paix, Paris",
    "is_private": false,
    "organizers": ["507f1f77bcf86cd799439011"],
    "participants": ["507f1f77bcf86cd799439011"],
    "has_shopping_list": true,
    "has_carpooling": true,
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/events`

Récupérer la liste des événements.

**Authentification requise**: Optionnelle (pour voir les événements privés)

**Paramètres de requête**:

| Paramètre | Type | Description |
|-----------|------|-------------|
| page | integer | Numéro de la page (défaut: 1) |
| per_page | integer | Items par page (défaut: 20) |
| group_id | string | Filtrer par groupe |

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "events": [
      {
        "_id": "507f1f77bcf86cd799439012",
        "name": "Soirée jeux de société",
        "description": "Une soirée sympa entre amis",
        "start_date": "2026-04-15T19:00:00Z",
        "location": "123 Rue de la Paix, Paris",
        "is_private": false
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 50,
      "pages": 3
    }
  }
}
```

---

### GET `/api/events/<event_id>`

Récupérer les détails d'un événement.

**Authentification requise**: Optionnelle (requise pour les événements privés)

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "_id": "507f1f77bcf86cd799439012",
    "name": "Soirée jeux de société",
    "description": "Une soirée sympa entre amis pour jouer",
    "start_date": "2026-04-15T19:00:00Z",
    "end_date": "2026-04-15T23:00:00Z",
    "location": "123 Rue de la Paix, Paris",
    "cover_photo": "https://example.com/event-cover.jpg",
    "is_private": false,
    "organizers": ["507f1f77bcf86cd799439011"],
    "participants": [
      "507f1f77bcf86cd799439011",
      "507f1f77bcf86cd799439013"
    ],
    "has_shopping_list": true,
    "has_carpooling": true,
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### PUT `/api/events/<event_id>`

Mettre à jour un événement.

**Authentification requise**: Oui  
**Restriction**: Seuls les organisateurs peuvent modifier

**Corps de la requête**:
```json
{
  "name": "Soirée jeux - MISE À JOUR",
  "description": "Description mise à jour",
  "start_date": "2026-04-15T20:00:00Z"
}
```

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Événement mis à jour avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439012",
    "name": "Soirée jeux - MISE À JOUR",
    "description": "Description mise à jour",
    "updated_at": "2026-02-02T15:00:00Z"
  }
}
```

---

### DELETE `/api/events/<event_id>`

Supprimer un événement.

**Authentification requise**: Oui  
**Restriction**: Seuls les organisateurs peuvent supprimer

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Événement supprimé avec succès",
  "data": null
}
```

---

### POST `/api/events/<event_id>/join`

Rejoindre un événement en tant que participant.

**Authentification requise**: Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Vous participez maintenant à l'événement",
  "data": null
}
```

---

### POST `/api/events/<event_id>/leave`

Quitter un événement.

**Authentification requise**: Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Vous avez quitté l'événement",
  "data": null
}
```

---

## 4. Groupes

### POST `/api/groups`

Créer un nouveau groupe.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "name": "Amis de l'université",
  "description": "Groupe pour les anciens de la Promo 2020",
  "icon": "https://example.com/icon.png",
  "cover_photo": "https://example.com/cover.jpg",
  "group_type": "private",
  "allow_members_to_post": true,
  "allow_members_to_create_events": true,
  "members": ["507f1f77bcf86cd799439013"]
}
```

**Champs requis**: `name`, `description`, `group_type`

**Types de groupe**:
- `public` - Visible par tous, tout le monde peut rejoindre
- `private` - Visible par tous, inscription sur demande
- `secret` - Invisible, uniquement sur invitation

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Groupe créé avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439020",
    "name": "Amis de l'université",
    "description": "Groupe pour les anciens de la Promo 2020",
    "group_type": "private",
    "allow_members_to_post": true,
    "allow_members_to_create_events": true,
    "administrators": ["507f1f77bcf86cd799439011"],
    "members": ["507f1f77bcf86cd799439011"],
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/groups`

Récupérer la liste des groupes.

**Authentification requise**: Optionnelle

**Paramètres**: `page`, `per_page`

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "groups": [
      {
        "_id": "507f1f77bcf86cd799439020",
        "name": "Amis de l'université",
        "description": "Groupe pour les anciens de la Promo 2020",
        "group_type": "private",
        "members_count": 15
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 8,
      "pages": 1
    }
  }
}
```

---

### GET `/api/groups/<group_id>`

Récupérer les détails d'un groupe.

**Authentification requise**: Optionnelle (requise pour groupes privés/secrets)

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "_id": "507f1f77bcf86cd799439020",
    "name": "Amis de l'université",
    "description": "Groupe pour les anciens de la Promo 2020",
    "group_type": "private",
    "allow_members_to_post": true,
    "allow_members_to_create_events": true,
    "administrators": ["507f1f77bcf86cd799439011"],
    "members": [
      "507f1f77bcf86cd799439011",
      "507f1f77bcf86cd799439013"
    ],
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### PUT `/api/groups/<group_id>`

Mettre à jour un groupe.

**Authentification requise**: Oui  
**Restriction**: Seuls les administrateurs peuvent modifier

**Corps de la requête**:
```json
{
  "name": "Nouveaux amis de l'université",
  "description": "Description mise à jour",
  "allow_members_to_post": false
}
```

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Groupe mis à jour avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439020",
    "name": "Nouveaux amis de l'université",
    "description": "Description mise à jour",
    "updated_at": "2026-02-02T15:00:00Z"
  }
}
```

---

### POST `/api/groups/<group_id>/join`

Rejoindre un groupe.

**Authentification requise**: Oui  
**Note**: Impossible de rejoindre un groupe secret sans invitation

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Vous êtes maintenant membre du groupe",
  "data": null
}
```

---

### POST `/api/groups/<group_id>/leave`

Quitter un groupe.

**Authentification requise**: Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Vous avez quitté le groupe",
  "data": null
}
```

---

## 5. Discussions

### GET `/api/discussions/event/<event_id>/messages`

Récupérer les messages d'un événement.

**Authentification requise**: Oui  
**Restriction**: Seuls les participants peuvent voir

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "messages": [
      {
        "_id": "507f1f77bcf86cd799439031",
        "author_id": "507f1f77bcf86cd799439011",
        "author_name": "John Doe",
        "content": "Salut tout le monde ! J'ai hâte d'être à samedi !",
        "parent_message_id": null,
        "created_at": "2026-02-01T12:00:00Z"
      }
    ]
  }
}
```

---

### POST `/api/discussions/event/<event_id>/messages`

Poster un message dans un événement.

**Authentification requise**: Oui  
**Restriction**: Seuls les participants peuvent poster

**Corps de la requête**:
```json
{
  "content": "Salut tout le monde ! J'ai hâte d'être à samedi !",
  "parent_message_id": null
}
```

Pour répondre à un message, spécifier `parent_message_id`:
```json
{
  "content": "Moi aussi !",
  "parent_message_id": "507f1f77bcf86cd799439031"
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Message posté avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439032",
    "author_id": "507f1f77bcf86cd799439011",
    "author_name": "John Doe",
    "content": "Salut tout le monde !",
    "parent_message_id": null,
    "created_at": "2026-02-01T12:00:00Z"
  }
}
```

---

### GET `/api/discussions/group/<group_id>/messages`

Récupérer les messages d'un groupe.

**Authentification requise**: Oui  
**Restriction**: Seuls les membres peuvent voir

---

### POST `/api/discussions/group/<group_id>/messages`

Poster un message dans un groupe.

**Authentification requise**: Oui  
**Restriction**: Seuls les membres peuvent poster (si autorisé)

---

## 6. Albums et Photos

### POST `/api/albums`

Créer un album photo.

**Authentification requise**: Oui  
**Restriction**: Seuls les participants de l'événement

**Corps de la requête**:
```json
{
  "name": "Photos de la soirée",
  "description": "Les meilleurs moments",
  "event_id": "507f1f77bcf86cd799439012"
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Album créé avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439040",
    "name": "Photos de la soirée",
    "description": "Les meilleurs moments",
    "event_id": "507f1f77bcf86cd799439012",
    "created_by": "507f1f77bcf86cd799439011",
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/albums/event/<event_id>`

Récupérer les albums d'un événement.

**Authentification requise**: Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "albums": [
      {
        "_id": "507f1f77bcf86cd799439040",
        "name": "Photos de la soirée",
        "event_id": "507f1f77bcf86cd799439012"
      }
    ]
  }
}
```

---

### POST `/api/albums/<album_id>/photos`

Ajouter une photo à un album.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "url": "https://example.com/photo.jpg",
  "caption": "Une belle photo de groupe !",
  "album_id": "507f1f77bcf86cd799439040"
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Photo ajoutée avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439041",
    "url": "https://example.com/photo.jpg",
    "caption": "Une belle photo de groupe !",
    "album_id": "507f1f77bcf86cd799439040",
    "posted_by": "507f1f77bcf86cd799439011",
    "posted_by_name": "John Doe",
    "comments": [],
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/albums/<album_id>/photos`

Récupérer les photos d'un album.

**Authentification requise**: Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "photos": [
      {
        "_id": "507f1f77bcf86cd799439041",
        "url": "https://example.com/photo.jpg",
        "caption": "Une belle photo de groupe !",
        "posted_by_name": "John Doe",
        "comments": []
      }
    ]
  }
}
```

---

### POST `/api/albums/photos/<photo_id>/comments`

Commenter une photo.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "content": "Super photo !"
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Commentaire ajouté avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439042",
    "author_id": "507f1f77bcf86cd799439013",
    "author_name": "Jane Smith",
    "content": "Super photo !",
    "created_at": "2026-02-01T11:00:00Z"
  }
}
```

---

## 7. Sondages

### POST `/api/polls`

Créer un sondage.

**Authentification requise**: Oui  
**Restriction**: Seuls les organisateurs

**Corps de la requête**:
```json
{
  "title": "Choix du menu",
  "description": "Votez pour votre menu préféré",
  "event_id": "507f1f77bcf86cd799439012",
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
  "allow_multiple_votes": false
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Sondage créé avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439050",
    "title": "Choix du menu",
    "event_id": "507f1f77bcf86cd799439012",
    "questions": [...],
    "responses": [],
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/polls/event/<event_id>`

Récupérer les sondages d'un événement.

**Authentification requise**: Oui

---

### POST `/api/polls/<poll_id>/respond`

Répondre à un sondage.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "responses": [
    {"question_index": 0, "option_index": 1},
    {"question_index": 1, "option_index": 0}
  ]
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Réponse enregistrée avec succès",
  "data": {
    "user_id": "507f1f77bcf86cd799439011",
    "user_name": "John Doe",
    "responses": [...],
    "created_at": "2026-02-01T12:00:00Z"
  }
}
```

---

### GET `/api/polls/<poll_id>/results`

Obtenir les résultats d'un sondage.

**Authentification requise**: Oui

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "poll": {...},
    "total_responses": 15,
    "results": [
      {
        "question": "Quel type de cuisine préférez-vous ?",
        "options": [
          {"option": "Italienne", "votes": 3},
          {"option": "Japonaise", "votes": 8},
          {"option": "Française", "votes": 2},
          {"option": "Mexicaine", "votes": 2}
        ]
      }
    ]
  }
}
```

---

## 8. Billetterie

### POST `/api/tickets/types`

Créer un type de billet.

**Authentification requise**: Oui  
**Restriction**: Seuls les organisateurs

**Corps de la requête**:
```json
{
  "name": "Billet Standard",
  "price": 25.00,
  "quantity": 100,
  "description": "Accès standard à l'événement",
  "event_id": "507f1f77bcf86cd799439012"
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Type de billet créé avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439060",
    "name": "Billet Standard",
    "price": 25.00,
    "quantity": 100,
    "remaining": 100,
    "event_id": "507f1f77bcf86cd799439012",
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/tickets/types/event/<event_id>`

Récupérer les types de billets d'un événement.

**Authentification requise**: Optionnelle

---

### POST `/api/tickets/purchase`

Acheter un billet.

**Authentification requise**: Non (route publique)

**Corps de la requête**:
```json
{
  "ticket_type_id": "507f1f77bcf86cd799439060",
  "buyer_first_name": "Marie",
  "buyer_last_name": "Dupont",
  "buyer_email": "marie.dupont@example.com",
  "buyer_address": {
    "street": "45 Rue de la République",
    "city": "Lyon",
    "postal_code": "69001",
    "country": "France"
  }
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Billet acheté avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439061",
    "ticket_type_id": "507f1f77bcf86cd799439060",
    "ticket_number": "T-507f1f77bcf86cd799439061",
    "buyer_first_name": "Marie",
    "buyer_last_name": "Dupont",
    "price_paid": 25.00,
    "purchase_date": "2026-02-01T14:00:00Z"
  }
}
```

---

### GET `/api/tickets/event/<event_id>`

Récupérer les billets vendus (organisateurs uniquement).

**Authentification requise**: Oui  
**Restriction**: Organisateurs uniquement

**Réponse (200)**:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "tickets": [...],
    "total_sold": 25,
    "total_revenue": 625.00
  }
}
```

---

## 9. Shopping List (BONUS)

### POST `/api/shopping`

Ajouter un item à la shopping list.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "name": "Chips",
  "quantity": 3,
  "arrival_time": "2026-04-15T19:30:00Z",
  "event_id": "507f1f77bcf86cd799439012",
  "notes": "Format familial"
}
```

**Note**: Le nom de l'item doit être unique par événement.

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Item ajouté avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439070",
    "name": "Chips",
    "quantity": 3,
    "arrival_time": "2026-04-15T19:30:00Z",
    "event_id": "507f1f77bcf86cd799439012",
    "user_id": "507f1f77bcf86cd799439011",
    "user_name": "John Doe",
    "notes": "Format familial",
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/shopping/event/<event_id>`

Récupérer la shopping list d'un événement.

**Authentification requise**: Oui

---

### PUT `/api/shopping/<item_id>`

Mettre à jour un item.

**Authentification requise**: Oui  
**Restriction**: Seul le créateur peut modifier

**Corps de la requête**:
```json
{
  "quantity": 5,
  "notes": "Format XXL finalement"
}
```

---

### DELETE `/api/shopping/<item_id>`

Supprimer un item.

**Authentification requise**: Oui  
**Restriction**: Seul le créateur peut supprimer

---

## 10. Covoiturage (BONUS)

### POST `/api/carpooling`

Créer une offre de covoiturage.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "departure_location": "Gare de Lyon, Paris",
  "departure_time": "2026-04-15T17:00:00Z",
  "price": 10.00,
  "available_seats": 3,
  "max_time_difference": 30,
  "event_id": "507f1f77bcf86cd799439012",
  "notes": "Musique autorisée, pas de fumée"
}
```

**Champ `max_time_difference`**: Temps d'écart maximum en minutes.  
Exemple: trajet de 2h30 + 30min d'écart = trajet max de 3h.

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Offre de covoiturage créée avec succès",
  "data": {
    "_id": "507f1f77bcf86cd799439080",
    "departure_location": "Gare de Lyon, Paris",
    "departure_time": "2026-04-15T17:00:00Z",
    "price": 10.00,
    "available_seats": 3,
    "total_seats": 3,
    "driver_id": "507f1f77bcf86cd799439011",
    "driver_name": "John Doe",
    "passengers": [],
    "created_at": "2026-02-01T10:00:00Z"
  }
}
```

---

### GET `/api/carpooling/event/<event_id>`

Récupérer les offres de covoiturage.

**Authentification requise**: Oui

---

### POST `/api/carpooling/<offer_id>/book`

Réserver une place.

**Authentification requise**: Oui

**Corps de la requête**:
```json
{
  "seats_requested": 2
}
```

**Réponse (201)**:
```json
{
  "success": true,
  "message": "Réservation effectuée avec succès",
  "data": {
    "user_id": "507f1f77bcf86cd799439013",
    "user_name": "Jane Smith",
    "seats_booked": 2,
    "booked_at": "2026-02-01T14:00:00Z"
  }
}
```

---

### POST `/api/carpooling/<offer_id>/cancel`

Annuler sa réservation.

**Authentification requise**: Oui

---

### PUT `/api/carpooling/<offer_id>`

Mettre à jour une offre.

**Authentification requise**: Oui  
**Restriction**: Seul le conducteur peut modifier

---

### DELETE `/api/carpooling/<offer_id>`

Supprimer une offre.

**Authentification requise**: Oui  
**Restriction**: Seul le conducteur peut supprimer (pas de passagers)

---

## Exemples d'utilisation

### Workflow complet : Créer un événement avec toutes les fonctionnalités

#### 1. S'inscrire
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

#### 2. Se connecter et obtenir le token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Sauvegarder le token retourné** :
```bash
export TOKEN="votre_token_jwt_ici"
```

#### 3. Créer un événement
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Soirée d anniversaire",
    "description": "Fête surprise pour Marie",
    "start_date": "2026-04-15T19:00:00Z",
    "end_date": "2026-04-15T23:00:00Z",
    "location": "123 Rue de la Paix, Paris",
    "is_private": true,
    "has_shopping_list": true,
    "has_carpooling": true
  }'
```

**Sauvegarder l'ID de l'événement** :
```bash
export EVENT_ID="507f1f77bcf86cd799439012"
```

#### 4. Ajouter un item à la shopping list
```bash
curl -X POST http://localhost:5000/api/shopping \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chips",
    "quantity": 3,
    "arrival_time": "2026-04-15T19:30:00Z",
    "event_id": "'$EVENT_ID'",
    "notes": "Format familial"
  }'
```

#### 5. Créer une offre de covoiturage
```bash
curl -X POST http://localhost:5000/api/carpooling \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "departure_location": "Gare de Lyon, Paris",
    "departure_time": "2026-04-15T17:00:00Z",
    "price": 10.00,
    "available_seats": 3,
    "max_time_difference": 30,
    "event_id": "'$EVENT_ID'"
  }'
```

#### 6. Créer un sondage
```bash
curl -X POST http://localhost:5000/api/polls \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Choix du menu",
    "event_id": "'$EVENT_ID'",
    "questions": [
      {
        "question": "Quel type de cuisine ?",
        "options": ["Italienne", "Japonaise", "Française"]
      }
    ]
  }'
```

#### 7. Poster un message
```bash
curl -X POST http://localhost:5000/api/discussions/event/$EVENT_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Super événement ! J ai hâte !"
  }'
```

---

## Bonnes pratiques

### 1. Sécurité

-  **Toujours utiliser HTTPS en production**
-  **Ne jamais partager votre token JWT**
-  **Renouveler les tokens régulièrement**
-  **Valider les données côté client avant envoi**

### 2. Performance

-  **Utiliser la pagination** pour les listes volumineuses
-  **Mettre en cache les données statiques**
-  **Limiter le nombre de requêtes simultanées**

### 3. Gestion des erreurs

-  **Toujours vérifier le code de statut HTTP**
-  **Lire le message d'erreur pour le debugging**
-  **Implémenter un système de retry pour les erreurs 500**

### 4. Format des dates

-  **Utiliser le format ISO 8601** : `2026-04-15T19:00:00Z`
-  **Toutes les dates sont en UTC**
-  **Convertir en heure locale côté client**

### 5. Validation

-  **Respecter les longueurs maximales des champs**
-  **Valider les formats d'email**
-  **Vérifier les dates (end_date > start_date)**

---

## Contact et Support

- **Email**: dissisalma@gmail.com
- **GitHub**:  https://github.com/SalmaDev-alt/my-social-networks-api
- **Documentation**: http://localhost:5000

---

**Version**: 1.0.0  
**Dernière mise à jour**: Février 2026  
**Auteur**: Salma DISSI

---

