# Guide d'Installation - My Social Networks API

Ce guide vous accompagne pas à pas dans l'installation et la configuration de l'API My Social Networks.

---

## Table des matières

1. [Prérequis](#prérequis)
2. [Installation locale](#installation-locale)
3. [Configuration MongoDB](#configuration-mongodb)
4. [Configuration de l'environnement](#configuration-de-lenvironnement)
5. [Lancement de l'application](#lancement-de-lapplication)
6. [Vérification de l'installation](#vérification-de-linstallation)
7. [Dépannage](#dépannage)

---

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

### Obligatoire
- **Python 3.8 ou supérieur** - [Télécharger Python](https://www.python.org/downloads/)
- **pip** (gestionnaire de paquets Python, généralement inclus avec Python)
- **Git** - [Télécharger Git](https://git-scm.com/downloads)

### Base de données (choisir une option)
- **Option A** : MongoDB local - [Télécharger MongoDB](https://www.mongodb.com/try/download/community)
- **Option B** : MongoDB Atlas (gratuit, recommandé) - [Créer un compte](https://www.mongodb.com/cloud/atlas/register)

### Recommandé pour les tests
- **Postman** - [Télécharger Postman](https://www.postman.com/downloads/)

---

## Installation locale

### Étape 1 : Cloner le repository

Ouvrez un terminal et exécutez :
```bash
# Cloner le projet
git clone https://github.com/SalmaDev-alt/my-social-networks-api.git

# Accéder au dossier du projet
cd my-social-networks-api
```

### Étape 2 : Créer un environnement virtuel

#### Sur Windows
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (PowerShell)
venv\Scripts\Activate.ps1

# OU sur CMD
venv\Scripts\activate.bat
```

#### Sur macOS/Linux
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate
```

**Note** : Vous devriez voir `(venv)` apparaître au début de votre ligne de commande.

### Étape 3 : Installer les dépendances
```bash
# Installer toutes les dépendances
pip install -r requirements.txt
```

**Dépendances installées :**
- Flask 3.0.0 - Framework web
- Flask-PyMongo 2.3.0 - Intégration MongoDB
- PyMongo 4.6.1 - Driver MongoDB
- PyJWT 2.9.0 - Gestion des tokens JWT
- bcrypt 4.1.2 - Hashage des mots de passe
- Marshmallow 3.20.1 - Validation des données
- flask-cors 4.0.0 - Gestion des CORS
- python-dotenv 1.0.0 - Variables d'environnement

---

## Configuration MongoDB

### Option A : MongoDB Atlas (Recommandé - Cloud gratuit)

#### 1. Créer un compte MongoDB Atlas

1. Allez sur [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Créez un compte gratuit
3. Choisissez le plan **M0 Sandbox** (Free)

#### 2. Créer un cluster

1. Sélectionnez votre région (ex: `Europe West (Ireland)`)
2. Nommez votre cluster (ex: `my-social-networks`)
3. Cliquez sur **Create Cluster**

#### 3. Configurer l'accès réseau

1. Dans le menu, allez sur **Network Access**
2. Cliquez sur **Add IP Address**
3. Sélectionnez **Allow Access from Anywhere** (`0.0.0.0/0`)
4. Cliquez sur **Confirm**

#### 4. Créer un utilisateur de base de données

1. Dans le menu, allez sur **Database Access**
2. Cliquez sur **Add New Database User**
3. **Username** : `admin` (ou votre choix)
4. **Password** : Générez un mot de passe fort (notez-le bien)
5. **Database User Privileges** : `Read and write to any database`
6. Cliquez sur **Add User**

#### 5. Obtenir la chaîne de connexion

1. Retournez sur **Database** et cliquez sur **Connect** sur votre cluster
2. Sélectionnez **Connect your application**
3. Choisissez **Driver** : `Python` et **Version** : `3.12 or later`
4. Copiez la chaîne de connexion (ressemble à) :
```
   mongodb+srv://admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```
5. **Remplacez `<password>`** par votre mot de passe réel

**Exemple de chaîne finale :**
```
mongodb+srv://admin:MonMotDePasse123@cluster0.ab1cd.mongodb.net/my_social_networks?retryWrites=true&w=majority
```

---

### Option B : MongoDB Local

#### Installation sur Windows

1. Téléchargez MongoDB Community Server : https://www.mongodb.com/try/download/community
2. Lancez l'installateur
3. Sélectionnez **Complete** installation
4. Cochez **Install MongoDB as a Service**
5. Terminez l'installation

MongoDB démarre automatiquement en tant que service.

**Chaîne de connexion locale :**
```
mongodb://localhost:27017/my_social_networks
```

#### Installation sur macOS
```bash
# Avec Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Démarrer MongoDB
brew services start mongodb-community
```

#### Installation sur Linux (Ubuntu/Debian)
```bash
# Importer la clé publique
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Ajouter le repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Installer MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Démarrer MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## Configuration de l'environnement

### Étape 1 : Créer le fichier .env
```bash
# Copier le template
cp .env.example .env

# Sur Windows PowerShell
copy .env.example .env
```

### Étape 2 : Éditer le fichier .env

Ouvrez le fichier `.env` dans un éditeur de texte et configurez :
```env
# Configuration MongoDB
# Option A : MongoDB Atlas (Cloud)
MONGO_URI=mongodb+srv://admin:VotreMotDePasse@cluster0.xxxxx.mongodb.net/my_social_networks?retryWrites=true&w=majority

# Option B : MongoDB Local
# MONGO_URI=mongodb://localhost:27017/my_social_networks

# Clés secrètes (CHANGEZ CES VALEURS EN PRODUCTION)
SECRET_KEY=votre_cle_secrete_super_securisee_a_changer_absolument
JWT_SECRET_KEY=votre_jwt_secret_key_super_securisee_a_changer

# Configuration de l'application
DEBUG=True
FLASK_ENV=development

# Dossier des uploads
UPLOAD_FOLDER=uploads

# Port (optionnel, par défaut 5000)
PORT=5000
```

### Étape 3 : Générer des clés secrètes sécurisées

Pour générer des clés aléatoires sécurisées :

#### Sur Python
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiez le résultat dans `SECRET_KEY` et générez-en un autre pour `JWT_SECRET_KEY`.

---

## Lancement de l'application

### Étape 1 : Activer l'environnement virtuel

Si ce n'est pas déjà fait :
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### Étape 2 : Lancer le serveur
```bash
python app.py
```

**Résultat attendu :**
```
MY SOCIAL NETWORKS API
Projet: API REST pour réseau social
Auteur: Salma
Date: Février 2026

Fonctionnalités disponibles:
   - Authentification JWT
   - Gestion des utilisateurs
   - Événements (publics/privés)
   - Groupes (public/privé/secret)
   - Discussions et messages
   - Albums photos avec commentaires
   - Sondages
   - Billetterie
   - Shopping list (BONUS)
   - Covoiturage (BONUS)

Serveur: http://localhost:5000
Mode: DEBUG
MongoDB: mongodb+srv://...

 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.32:5000
```

### Étape 3 : Garder le serveur actif

**Laissez ce terminal ouvert** tant que vous utilisez l'API.

Pour arrêter le serveur : `Ctrl + C`

---

## Vérification de l'installation

### Test 1 : Vérifier la connexion à l'API

Ouvrez un nouveau terminal (ou navigateur) et testez :
```bash
# Avec curl
curl http://localhost:5000

# Ou dans un navigateur
http://localhost:5000
```

**Résultat attendu :** Un JSON avec les informations de l'API

### Test 2 : Vérifier la santé de l'API
```bash
curl http://localhost:5000/api/health
```

**Résultat attendu :**
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "API is running smoothly"
}
```

Si `"database": "connected"`, MongoDB fonctionne correctement.  
Si `"database": "disconnected"`, vérifiez votre configuration MongoDB.

### Test 3 : S'inscrire (premier utilisateur)

#### Avec curl
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\",\"first_name\":\"Test\",\"last_name\":\"User\"}"
```

#### Avec Postman

1. Méthode : `POST`
2. URL : `http://localhost:5000/api/auth/register`
3. Headers : `Content-Type: application/json`
4. Body (raw JSON) :
```json
{
  "email": "test@example.com",
  "password": "password123",
  "first_name": "Test",
  "last_name": "User"
}
```

**Résultat attendu :**
```json
{
  "success": true,
  "message": "Utilisateur créé avec succès",
  "data": {
    "user": { ... },
    "token": "eyJhbGc..."
  }
}
```

**Installation réussie.** Vous pouvez maintenant utiliser l'API.

---

## Dépannage

### Problème 1 : "No module named 'flask'"

**Cause :** Les dépendances ne sont pas installées.

**Solution :**
```bash
# Vérifier que l'environnement virtuel est activé (vous devriez voir (venv))
pip install -r requirements.txt
```

### Problème 2 : "ModuleNotFoundError: No module named 'dotenv'"

**Solution :**
```bash
pip install python-dotenv
```

### Problème 3 : MongoDB "Connection refused" ou "disconnected"

**Causes possibles :**
- MongoDB n'est pas démarré (local)
- Mauvaise chaîne de connexion
- Problème de réseau (Atlas)

**Solutions :**

#### Pour MongoDB local :
```bash
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

#### Pour MongoDB Atlas :
- Vérifiez que votre IP est autorisée (0.0.0.0/0)
- Vérifiez le mot de passe dans `MONGO_URI`
- Vérifiez que vous avez remplacé `<password>` par votre vrai mot de passe

### Problème 4 : Port 5000 déjà utilisé

**Solution :** Changer le port dans `.env`
```env
PORT=5001
```

Puis relancez l'application.

### Problème 5 : "ImportError" diverses

**Solution :** Réinstaller toutes les dépendances
```bash
# Désinstaller tout
pip freeze | xargs pip uninstall -y

# Réinstaller
pip install -r requirements.txt
```

### Problème 6 : Erreur de permissions (Linux/macOS)

**Solution :**
```bash
# Donner les permissions d'exécution
chmod +x app.py

# Ou installer avec --user
pip install --user -r requirements.txt
```

---

## Prochaines étapes

Une fois l'installation terminée :

1. **Consultez la documentation** : [docs/api_documentation.md](docs/api_documentation.md)
2. **Testez avec Postman** : [Collection Postman](postman/README.md)
3. **Explorez les endpoints** : Consultez le [README.md](README.md)

---

## Besoin d'aide ?

Si vous rencontrez des problèmes non listés ici :

1. Vérifiez les **logs** dans le terminal où tourne le serveur
2. Assurez-vous que toutes les **dépendances** sont installées
3. Vérifiez votre **configuration MongoDB**
4. Consultez la documentation MongoDB Atlas : https://docs.atlas.mongodb.com/

---

## Notes importantes

### Sécurité

**En production**, pensez à :
- Changer les clés secrètes (`SECRET_KEY`, `JWT_SECRET_KEY`)
- Mettre `DEBUG=False`
- Utiliser des mots de passe forts pour MongoDB
- Restreindre l'accès réseau MongoDB (pas 0.0.0.0/0)
- Activer HTTPS

### Performance

Pour de meilleures performances en production :
- Utilisez **Gunicorn** ou **uWSGI** au lieu du serveur Flask de développement
- Configurez un **reverse proxy** (Nginx, Apache)
- Activez le **caching** avec Redis
- Utilisez un **load balancer** si nécessaire

---

**Installation terminée. Votre API est prête à l'emploi.**