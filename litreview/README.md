# LITReview – Plateforme communautaire de critiques de livres

## Description du projet

**LITReview** est une application web développée avec **Django** permettant aux utilisateurs de :

* publier une demande de critique d’un livre (ticket),
* rédiger des critiques,
* suivre d’autres lecteurs,
* consulter un flux personnalisé d’actualités.


---

## Objectifs du projet

L’objectif est de développer une plateforme communautaire fonctionnelle en respectant une architecture backend Django et un système d’authentification utilisateur.

Le projet repose sur :

* une architecture **MVT Django**,
* un système de comptes utilisateurs,
* la gestion des relations entre modèles,
* des formulaires sécurisés,
* une interface responsive avec **Tailwind CSS**.

---

## Fonctionnalités

### Authentification

* Création de compte
* Connexion / Déconnexion
* Gestion d’un utilisateur personnalisé (`CustomUser`)

### Tickets

* Création d’un ticket
* Modification d’un ticket
* Suppression d’un ticket
* Ajout d’image facultatif

### Critiques

* Création d’une critique
* Modification d’une critique
* Suppression d’une critique
* Système de notation sur 5

### Abonnements

* Suivre un utilisateur
* Se désabonner d’un utilisateur
* Consultation des utilisateurs suivis

### Flux personnalisé

Le flux affiche :

* les tickets publiés par l’utilisateur,
* les critiques des utilisateurs suivis,
* les critiques des livres demandés par l’utilisateur.

Le tout trié par ordre chronologique.

---

## Technologies utilisées

### Backend

* Python 3
* Django 6

### Frontend

* HTML5
* Tailwind CSS

### Base de données

* SQLite3

---

## Installation du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-compte/litreview.git
cd litreview
```

 ### 2. Créer un environnement virtuel

python -m venv .venv
.venv\Scripts\activate


### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. création de l'application AppCritique
Tout d'abord, on crée le projet Django avec la commande : 
```bash
django-admin startproject litreview
```
Par la suite, on se position dans le projet en tappant la commande : ```bash  cd litreview``` et crée l'application Django

```bash
python manage.py startapp AppCritique

```
L'application va ensuite être rajouter dans le fichier settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AppCritique', # ajout de l'application métier : AppCritique 
]

Lance les commandes ci-dessous pour générer les migrations 
```bash
python manage.py makemigrations
python manage.py migrate
```




### 5. Créer un superutilisateur (admin)

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement 

```bash
python manage.py runserver
```

Accéder ensuite à :

```text
http://127.0.0.1:8000/
```

---

## Accès administration Django

Interface admin disponible ici :

```text
http://127.0.0.1:8000/admin/
```

Créer un superutilisateur avec :

```bash
python manage.py createsuperuser
```

---

## Structure du projet

```text
litreview/
│── AppCritique/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
│── litreview/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
│── media/
│── db.sqlite3
│── manage.py
│── requirements.txt
│── README.md
```

---

## Aperçu des modèles de données

### User

Utilisateur personnalisé hérité de Django :

* username
* email
* password

### Ticket

Permet de demander une critique :

* titre
* description
* image
* auteur
* date de création

### Review

Permet de publier une critique :

* note sur 5
* titre
* contenu
* ticket associé
* auteur

### UserFollows

Gestion des abonnements :

* utilisateur
* utilisateur suivi

---

## Sécurité et bonnes pratiques implémentées

* Authentification Django sécurisée
* Protection CSRF sur les formulaires
* Permissions utilisateur sur les modifications/suppressions
* Restriction des actions aux auteurs des contenus
* Gestion des accès avec `@login_required`

---

