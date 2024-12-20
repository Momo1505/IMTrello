# IMTrello

## Description
Ce projet est une application web de gestion de tâches conçue pour faciliter la collaboration au sein d'une équipe de développement. L'application permet à certains utilisateurs privilégiés de créer des projets, d'ajouter des tâches à ces projets et de les attribuer à des membres de l'équipe. Les utilisateurs sont répartis en deux rôles principaux : les développeurs et les chefs de projet. Chaque dévéloppeur peut se connecter à l'application, consulter les tâches qui lui sont assignées dans le projet.

## Fonctionnalités Principales
- **Authentification Utilisateur** : Les utilisateurs peuvent s'inscrire, se connecter et se déconnecter.
- **Gestion des Projets** : Les project manager peuvent créer de nouveaux projets.
- **Gestion des Tâches** : Les project manager peuvent ajouter de nouvelles tâches à un projet existant, les attribuer à des membres de l'équipe et suivre l'etat des taches dans le projet.
- **Gestion des Rôles** : Les utilisateurs sont répartis en deux rôles principaux : développeurs et chefs de projet.

## Structure du Projet
Le projet est organisé en plusieurs packages Flask :

- **App** : Package principal contenant les configurations générales de l'application.
  - **Authentification** : Package gérant l'authentification des utilisateurs.
  - **Main** : Package contenant les vues et les fonctionnalités principales de l'application.
  - **Models** : fichier python contenant les modèles de base de données.
- **Templates** : Dossier contenant les fichiers HTML pour l'interface utilisateur.
- **Static** : Dossier contenant les fichiers statiques tels que les feuilles de style CSS et les scripts JavaScript.

## Technologies Utilisées
- **Flask** : Framework web en Python pour le backend.
- **Flask-Bootstrap** : Extension Flask pour l'intégration de Bootstrap pour le front-end.
- **Flask-WTF** : Extension Flask pour la création de formulaires web.
- **Flask-SQLAlchemy** : Extension Flask pour l'intégration d'une base de données SQLAlchemy.
- **Flask-Login** : Extension Flask pour la gestion de l'authentification des utilisateurs.
- **Flask-Migrate** : Extension Flask qui permettra de mettre à jour la base de données lorsqu'on apporte une modification ou ajout d'un attribut dans une table déjà existante (sinon, il faudra la supprimer à chaque fois qu'on modifie quelque chose) 

## Installation
1. Cloner le repository GitHub.
2. Installer les dépendances Python : `pip install -r requirements.txt`.
3. Configurer les variables d'environnement ou le fichier de configuration.
4. Exécuter l'application : Aller sur app.py pour lancer le projet.

## Contributeurs
- [SOW Mouhamed]
- [BONDKA Mouadh]
- [DIARISSO Abdoulaye]
