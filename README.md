# Coordination frontend / backend

## Contenu du repository
Ce repository est constitué d'une application fullstack :
- Base de donnée **Postgresql** accessible sur le port `5440`
- Backend **Flask** accessible sur le port `5005`
- Frontend **Next JS** accessible sur le port `3000`
- Moteur GraphQL **Hasura** accessible sur le port `8080`

Le backend utilise l'ORM SQLAlchemy et possède trois modèles :
- User
- Company
- Product

Le frontend permet le CRUD du modèle *Product*

## Prérequis
La stack nécessite `docker` et `docker compose` pour fonctionner.

## Lancement de la stack
Veuillez réaliser les étapes suivantes pour executer la stack :
- **Backend** : Créez un fichier `.env` à partir du `.env-template` et complétez le avec les informations nécessaires.
- **Frontend** : Créez un fichier `.env.local` à partir du `.env-template` et complétez le avec les informations nécessaires.

Pour lancer la stack, executez la commande suivante :  
`docker compose watch`

Au lancement, le service `db_migration_course_fullstack` s'occupera d'appliquer les migrations de base de données managées par `SQLAlchemy`.

## Utilisation
Après le lancement, accèdez au backend flask à l'URL suivante pour vous créer un compte http://localhost:5005/register. Vous pourrez ensuite aller sur http://localhost:5005/login pour vous connecter.
L'API swagger est disponible à l'URL suivante :  
http://localhost:5005/apidocs

Depuis Swagger, créez une `Company` depuis l'endpoint correspondant pour pouvoir par la suite y associer des produits depuis le frontend.