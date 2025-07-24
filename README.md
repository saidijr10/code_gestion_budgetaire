# 💼 Application de Gestion Budgétaire

Bienvenue dans l'application de **gestion budgétaire**, une plateforme web moderne développée avec **Vue.js** (frontend) et **Django REST Framework** (backend), permettant de gérer les budgets annuels, les lignes budgétaires, les prestataires, les clients, les ordonnancements et les règlements. Elle permet également l'import/export de fichiers Excel et la génération automatique de documents PDF.

---

## ✨ Fonctionnalités principales

- 👥 **Gestion des clients et prestataires**
  - Création, modification, suppression
  - Association à des ordonnancements ou règlements

- 📊 **Gestion des lignes budgétaires**
  - Chaque ligne appartient à un **budget d’une année donnée**
  - Suivi du montant total, du montant engagé, disponible et réglé

- 🔁 **Import / Export Excel**
  - Importation des lignes budgétaires et des règlements
  - Export des états budgétaires ou ordres de virement au format Excel

- 🧾 **Gestion des ordonnancements et des règlements**
  - Création d’ordonnancements par ligne budgétaire
  - Association aux prestataires
  - Suivi des paiements

- 📄 **Génération automatique de documents PDF**
  - **Fiche d’ordonnancement**
  - **Ordre de virement** avec détails bancaires
---

## 🛠️ Stack technique

- **Frontend** : Vue.js 3, Vue Router, Tailwind CSS
- **Backend** : Django, Django REST Framework
- **Base de données** : SQLite (dev) ou PostgreSQL (prod)
- **Outils Excel** : `pandas`, `openpyxl`
- **Génération PDF** : `WeasyPrint` ou `ReportLab`

---

## ⚙️ Installation du projet

### 1. Cloner le projet

```bash
git clone https://github.com/saidijr10/code_gestion_budgetaire.git
cd code_gestion_budgetaire

cd backend
python -m venv env
source env/bin/activate  # sous Windows : env\Scripts\activate
python manage.py migrate
python manage.py runserver


cd frontend
npm install
npm run serve

Interface utilisateur disponible sur : http://localhost:5000



