# Documentation du projet HomeFlix

## Structure du projet

Ce projet est divisé en deux parties principales : **Backend** et **Frontend**. Voici une description détaillée de chaque section.

---

## **Backend**

### Description des fichiers

1. **mainv2.py** : 
   Ce fichier contient le serveur de l'application backend utilisant **FastAPI**. Il définit les points de terminaison de l'API pour recommander des films et prédire des notes, ainsi que les modèles de réponse pour les recommandations et les prédictions.

2. **recommender.py** :
   Ce fichier implémente la logique des recommandations de films et de prédiction des notes des films pour un utilisateur spécifique. Il utilise un modèle **SVD** (Singular Value Decomposition) entraîné, qui est chargé lors du démarrage du serveur.

3. **load_data.py** :
   Ce fichier charge et prépare les données à partir de la base de données **DuckDB**. Il est responsable de l'établissement de la connexion avec la base de données et du chargement des tables `ratings` et `films` nécessaires au système de recommandation.

4. **utils/db.py** :
   Ce fichier contient une fonction (`load_data`) qui établit la connexion à **DuckDB** en mode lecture seule, extrayant les tables `ratings` et `films` pour leur utilisation dans le backend.

5. **models/svd_model.pkl** :
   Ce fichier contient le modèle **SVD** entraîné, utilisé pour les recommandations. Ce modèle est chargé lors du démarrage de l'application backend.

### Fonctionnement

Le backend est une API RESTful développée avec **FastAPI**, permettant au frontend d'interagir avec le système de recommandation de films. Il utilise un modèle de **SVD** pour faire des recommandations personnalisées et prédire les notes des films pour un utilisateur donné. Les données nécessaires (ratings et films) sont stockées dans une base de données **DuckDB**, qui est chargée au démarrage de l'application.

- L'endpoint `/recommend_movies/{user_id}` renvoie une liste de recommandations de films personnalisées pour un utilisateur donné.
- L'endpoint `/predict_rating/{user_id}/{movie_id}` prédit la note qu'un utilisateur donné attribuerait à un film donné.
- L'endpoint `/films` renvoie la liste des films disponibles.
- L'endpoint `/ratings` renvoie les évaluations des films faites par les utilisateurs.

---

## **Frontend**

### Description des fichiers

1. **app.py** :
   Ce fichier contient le code de l'application **Streamlit**, qui sert d'interface utilisateur pour le système. Il définit deux sections principales :
   - **Data Analysis** : Visualisation des statistiques des évaluations des films et du nombre de films sortis chaque année.
   - **Movie Recommendations** : Permet aux utilisateurs d'obtenir des recommandations de films personnalisées en fonction de leur ID utilisateur.

   Le frontend se connecte au backend via les points de terminaison définis dans **FastAPI**. Les informations sur les films et les recommandations sont récupérées via des requêtes HTTP.

2. **static/icon.png** :
   Contient une icône pour l'interface utilisateur de l'application (MAURICIO)


### Fonctionnement

Le frontend est une application **Streamlit** qui affiche une interface interactive permettant aux utilisateurs de visualiser des statistiques sur les films et de recevoir des recommandations personnalisées. Le frontend communique avec le backend via des requêtes HTTP et affiche les résultats sous forme de visualisations interactives et de listes de recommandations.

---

## **Instructions pour lancer le projet**

### Prérequis

1. **Dépendances** :
   - Pour le **backend**, assurez-vous d'installer toutes les dépendances nécessaires définies dans le fichier `requirements.txt` dans le dossier `backend`.
   - Pour le **frontend**, installez également les dépendances définies dans le fichier `requirements.txt` dans le dossier `frontend`.

2. **Base de données** :
   Avant de lancer le projet, il est nécessaire de charger les données dans la base de données **DuckDB**. Pour cela :
   
   - Exécutez le fichier `load_data.py` dans le dossier `backend` pour charger les données dans la base de données.
   - Assurez-vous d'ajouter le fichier CSV des évaluations (`ratings.csv`) dans le dossier `data` de votre projet, afin que le backend puisse y accéder.

---

### Lancer le projet avec Docker

Le projet est configuré pour être exécuté via Docker en utilisant le fichier `docker-compose.yml`. Pour lancer les services backend et frontend en utilisant Docker, suivez les étapes ci-dessous.

1. **Construire et lancer les conteneurs Docker** :

   Dans le dossier principal du projet, exécutez la commande suivante pour construire et démarrer les conteneurs :

   ```bash
   docker-compose up --build

2. **Accéder au frontend** :

    Une fois les conteneurs lancés, vous pouvez accéder à l'interface utilisateur Streamlit du frontend à l'adresse suivante :


    http://localhost:8501

    L'application Streamlit vous permettra de visualiser les recommandations de films et les statistiques des évaluations.

3. **Problème lors de la dockerisation**

    Lors de la tentative de dockerisation du projet, un problème se produit dans la communication entre le frontend et le backend. L'erreur obtenue est la suivante :

    La section de recommandations de films génère un message d'erreur :
    
    ```bash
    Failed to connect to backend at http://backend:8000: HTTPConnectionPool(host='backend', port=8000): Max retries exceeded with url: /recommend_movies/1 (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x7f082e752e10>: Failed to resolve 'backend' ([Errno -2] Name or service not known)")) 

4. **Analyse du problème**

    En analysant les messages d'erreur, il semble que le problème provient d'une mauvaise connexion entre le frontend et le backend lors de l'exécution des conteneurs Docker. Le frontend tente de se connecter au backend via l'URL http://backend:8000, mais nous obtenons une erreur indiquant qu'il est impossible de résoudre l'hôte backend.

    Nous avons vérifié les points suivants :

    La configuration du réseau Docker : les deux services sont connectés au même réseau (flix_network), ce qui devrait théoriquement permettre la communication entre eux.

    Le conteneur du backend se ferme  après son démarrage, et les journaux ne fournissent pas suffisamment d'informations pour identifier la cause du problème. L'erreur la plus fréquente dans les journaux est la suivante :

    ```bash
    INFO:     Started server process [1]
    INFO:     Waiting for application startup.

5. **Actions entreprises**

    Nous avons redémarré les conteneurs après avoir modifié la configuration du réseau dans le fichier docker-compose.yml.

    Nous avons augmenté le niveau des logs pour obtenir plus de détails sur le démarrage du backend.

    Nous avons vérifié les ressources système pour nous assurer qu'il n'y avait pas de limitations, mais le problème persiste.

6. **Conclusion**

    Le projet HomeFlix est un système de recommandation de films utilisant FastAPI pour le backend et Streamlit pour le frontend. Le système fonctionne correctement lorsque l'application est lancée manuellement, mais lors de la dockerisation, une erreur se produit lors de la communication entre les conteneurs frontend et backend. Nous avons tenté de résoudre ce problème en ajustant la configuration du réseau Docker et en augmentant les logs, mais la cause exacte du problème reste difficile à identifier.

    En attendant, le projet fonctionne normalement **en dehors de Docker**, et le système de recommandation ainsi que l'interface Streamlit sont **pleinement opérationnels dans un environnement local bien configuré**.

En raison du problème rencontré lors de la Dockerisation, nous avons laissé le projet configuré pour une exécution locale, comme expliqué au début du document. Assurez-vous que les chemins d’accès aux fichiers et aux ressources soient bien définis pour le système de fichiers local.
 






    