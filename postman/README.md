\# Collection Postman - My Social Networks API



\## Accéder à la collection


Lien documentation Postman : https://documenter.getpostman.com/view/44390291/2sBXc8p3yR#cc25a382-ef3c-4001-b668-5db2a4321e7f


\*\*Lien direct :\*\* \[My Social Networks API - Collection Postman](https://web.postman.co/workspace/My-Workspace~652b25ac-3c25-4b97-8738-a34692fe8f1f/collection/44390291-58b0d663-092c-43d0-a6ca-523114be6f24?action=share\&source=copy-link\&creator=44390291)





Cliquez sur le lien ci-dessus pour voir tous les tests effectués sur l'API.



\## Comment utiliser



1\. Cliquez sur le lien de la collection

2\. Dans Postman, cliquez sur \*\*"Fork Collection"\*\* ou \*\*"Import"\*\*

3\. La collection sera importée dans votre workspace

4\. Configurez l'URL de base : `http://localhost:5000`



\##  Tests inclus dans la collection



\###  Authentification (3 endpoints)

\- `POST /api/auth/register` - Inscription d'un nouvel utilisateur

\- `POST /api/auth/login` - Connexion et récupération du token JWT

\- `GET /api/auth/me` - Récupération du profil utilisateur connecté



\###  Connexion (1 endpoint)

\- `GET /api/auth/connexion` - Vérification de la connexion



\###  Mon profil (1 endpoint)

\- `GET /api/auth/mon-profil` - Consultation du profil



\###  Événements (7 endpoints)

\- `POST /api/events` - Créer un nouvel événement

\- `GET /api/events` - Liste de tous les événements

\- `GET /api/events/{id}` - Détails d'un événement

\- `PUT /api/events/{id}` - Modifier un événement

\- `DELETE /api/events/{id}` - Supprimer un événement

\- `POST /api/events/{id}/join` - Rejoindre un événement (rejoindreEvent)

\- `POST /api/events/{id}/leave` - Quitter un événement



\###  Groupes (6 endpoints)

\- `POST /api/groups` - Créer un groupe (create\_group)

\- `GET /api/groups` - Liste des groupes

\- `GET /api/groups/{id}` - Détails d'un groupe

\- `PUT /api/groups/{id}` - Modifier un groupe

\- `POST /api/groups/{id}/join` - Rejoindre un groupe

\- `POST /api/groups/{id}/leave` - Quitter un groupe



\###  Discussions (2 endpoints)

\- `GET /api/discussions/messages` - Liste des messages (post\_message)

\- `POST /api/discussions/messages` - Poster un message



\###  Sondages (1 endpoint)

\- `POST /api/polls` - Créer un sondage (créer\_sondage)



\###  Shopping List - BONUS (1 endpoint)

\- `POST /api/shopping` - Ajouter un item à la liste (add\_item\_shopping\_list)



\###  Covoiturage - BONUS (1 endpoint)

\- `POST /api/carpooling` - Créer une offre de covoiturage (créer\_offre\_covoiturage)



\###  Statistiques (1 endpoint)

\- `GET /api/stats` - Voir les statistiques de l'API (voir\_statistiques)



\##  Résultats des tests



\*\*Total : 24+ endpoints testés\*\*



Tous les tests ont été effectués avec succès :

\-  Codes de statut HTTP corrects (200, 201, 400, 401, 403, 404)

\-  Format JSON valide pour toutes les réponses

\-  Validation des données fonctionnelle

\-  Authentification JWT opérationnelle

\-  Gestion des permissions et autorisations vérifiée

\-  Fonctionnalités BONUS testées (Shopping list, Covoiturage)



\##  Configuration



\### Variables d'environnement recommandées



Pour faciliter les tests, créez ces variables dans Postman :

```json

{

&nbsp; "base\_url": "http://localhost:5000",

&nbsp; "token": "",

&nbsp; "event\_id": "",

&nbsp; "group\_id": "",

&nbsp; "poll\_id": ""

}

```



\### Workflow de test recommandé



1\. \*\*Inscription\*\* → Copier le token retourné

2\. \*\*Connexion\*\* → Vérifier le token

3\. \*\*Créer un événement\*\* → Copier l'ID de l'événement

4\. \*\*Rejoindre l'événement\*\* avec un autre utilisateur

5\. \*\*Tester les autres fonctionnalités\*\* (sondages, shopping, covoiturage)



\##  Validation complète



L'API a été entièrement testée et validée :

\- Tous les endpoints principaux fonctionnent

\- Les fonctionnalités BONUS sont opérationnelles

\- La sécurité JWT est correctement implémentée

\- Les validations de données sont en place

\- Les permissions sont respectées

