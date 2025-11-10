💰 Gestion Budgétaire

Une application web de gestion budgétaire permettant de suivre les revenus, dépenses et soldes.
Projet full-stack développé avec Django REST Framework (backend) et Vue.js (frontend).

⚙️ Prérequis

Avant de commencer, assure-toi d’avoir installé sur ta machine :

Python 3.x

Node.js & npm

Git

🧩 Backend — Django REST Framework
Étape 1 : Création du dossier et environnement virtuel
mkdir gestion-budgetaire
cd gestion-budgetaire

python -m venv env
env\Scripts\activate  # sous Windows
# ou
source env/bin/activate  # sous Mac/Linux

Étape 2 : Installation des dépendances
pip install django djangorestframework django-cors-headers pandas openpyxl

Étape 3 : Création du projet et de l’application
django-admin startproject backend
cd backend
python manage.py startapp budget_app

Étape 4 : Configuration de backend/settings.py

INSTALLED_APPS :

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'budget_app',
]


MIDDLEWARE (au début) :

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]


À la fin du fichier :

CORS_ALLOW_ALL_ORIGINS = True

Étape 5 : Migration de la base de données
python manage.py makemigrations
python manage.py migrate

Étape 6 : Lancer le serveur backend
python manage.py runserver


Le backend sera disponible sur http://127.0.0.1:8000/

🎨 Frontend — Vue.js
Étape 1 : Installer Vue CLI
npm install -g @vue/cli

Étape 2 : Créer le projet frontend
vue create frontend
cd frontend

Étape 3 : Lancer le serveur frontend
npm run serve


Le frontend sera accessible sur http://localhost:8080/

Étape 4 : Installer Vue Router (si nécessaire)
npm install vue-router@4

📂 Structure du projet
gestion-budgetaire/
│
├── backend/
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── budget_app/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   └── manage.py
│
└── frontend/
    ├── src/
    ├── package.json
    └── ...

🧠 Technologies utilisées

Backend : Django, Django REST Framework

Frontend : Vue.js, Vue Router

Autres : Pandas, OpenPyXL (pour traitement et export de données)

🚀 Lancement complet du projet

1️⃣ Lancer le backend :

cd backend
python manage.py runserver


2️⃣ Lancer le frontend :

cd ../frontend
npm run serve

🧾 Auteur

👨‍💻 Soufiane Saidi
