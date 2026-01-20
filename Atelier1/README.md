# 🎯 Valorant Analytics - Data Warehouse Project

Ce projet a pour but de structurer et d'analyser les performances e-sport sur le jeu **Valorant**. Nous utilisons une approche "Data Engineering" légère pour ingérer, modéliser et requêter des statistiques de jeu détaillées.

## 👥 Équipe

* **Samuel RESSIOT**
* **Rudolph ATTISSO**
* **Yassine ZOUITNI**

## 🛠️ Stack Technique

L'architecture est "Serverless" et contenue localement, conformément aux contraintes de l'atelier.

* **Application :** Python (Jupyter Notebook) pour l'orchestration et la visualisation.
* **Stockage & Requêtage :** [DuckDB](https://duckdb.org/) (Base de données analytique in-process).
* **Gestion de version :** Git / GitHub.

## 📊 Le Jeu de Données

Les données proviennent de statistiques de compétitions professionnelles de Valorant. Elles permettent d'analyser la méta du jeu (équilibrage) ainsi que les performances individuelles.

* **Lien vers la source :** https://www.kaggle.com/datasets/evangower/valorant-esports-top-earnings

### Contenu et Caractéristiques

Le dataset est composé de 4 fichiers CSV principaux reliés logiquement :

1.  **`players.csv`** (Performances Joueurs) :
    * Contient les statistiques individuelles par joueur (Rating, ACS - Average Combat Score, K/D Ratio, Headshot %).
    * Permet d'identifier les meilleurs joueurs par rôle ou par région.

2.  **`teams.csv`** (Performances Équipes) :
    * Agrège les résultats par équipe (Taux de victoire, succès en attaque vs défense, taux de victoire au "Pistol Round").

3.  **`agents.csv`** (Méta-jeu) :
    * Détaille les statistiques par personnage/agent (Taux de sélection "Pick rate", statistiques moyennes de K/D et de dégâts par agent).
    * Essentiel pour comprendre l'équilibrage du jeu.

4.  **`maps.csv`** (Cartographie) :
    * Statistiques liées aux cartes (Ascent, Bind, Haven, etc.).
    * Inclut les taux de victoire par côté (Attaque vs Défense) et les temps moyens de pose du Spike.

### Volumétrie et Pertinence
Ce jeu de données couvre des dizaines de milliers de manches (rounds) et offre une granularité fine ("In-game stats") telle que le **First Blood Rate** (FBPR) ou l'**Average Damage per Round** (ADR), dépassant le simple score final des matchs.



## 🚀 Installation et Utilisation

1.  Cloner le dépôt :
    ```bash
    git clone https://github.com/Sam-rst/EPSI_M1-Datamart
    cd EPSI_M1-Datamart/Atelier1
    ```

2.  Créer l'environnement virtuel et installer les dépendances (avec UV) :
    ```bash
    uv sync
    ```

3.  Lancer le notebook :
    Ouvrir le fichier `analysis.ipynb` (ou le nom de votre notebook) dans VS Code ou Jupyter Lab.


## 📖 Dictionnaire de Données

Les données contiennent de nombreux acronymes spécifiques à Valorant (ACS, ADR, FBPR...). 
Pour faciliter l'analyse, nous avons documenté chaque variable en détail.

👉 **[Consulter le Dictionnaire des Données complet](./docs/DATA_DICTIONARY.md)**

*(Ce document explique les méthodes de calcul des scores et la signification des métriques e-sport).*