# Projet 9 - Développez une application Web en utilisant Django

Le projet consiste à créer un site de critique de livres et d'articles. Les utilisateurs pourront demander une critique
d'un livre, répondre à une critique ou consulter les critiques des utilisateurs auxquels il est abonné.  

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- Git
- Python 3.11

## Installation

Suivez ces étapes pour installer et configurer le projet sur votre machine locale.

### Cloner le Répertoire

Pour récupérer le projet depuis Git, ouvrez votre terminal, aller dans le dossier où vous souhaitez cloner le projet et
exécuter la commande suivante :

git clone https://github.com/LeJinge/Projet_9.git

### Configurer l'Environnement Virtuel

Créez un environnement virtuel pour gérer les dépendances de manière isolée :

- Sur Windows :

python -m venv .env

.\env\Scripts\activate

- Sur Unix ou MacOS :

source .env/bin/activate

- Sur Git Bash :

python -m venv .env

source .env/Scripts/activate

### Installer les Dépendances

Installez toutes les dépendances nécessaires en utilisant :

pip install -r requirements.txt

## Lancement du Serveur de Développement

Pour lancer le serveur de développement, exécutez :

cd src

python manage.py runserver

Naviguez vers `http://127.0.0.1:8000/login` dans votre navigateur pour voir l'application en action.

