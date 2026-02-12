# 🎯 Projet Atelier 1 — Analyse de parties (Rocket League)

Ce dépôt contient un projet d'analyse et d'entreposage de données pour des parties de **Rocket League**. L'objectif est de structurer, charger et exploiter des statistiques "in-game" détaillées (mouvement, boost, positionnement, tirs, etc.) afin de pouvoir interroger et visualiser les performances.

## 👥 Équipe

- **Samuel RESSIOT**
- **Rudolph ATTISSO**
- **Yassine ZOUITNI**

## 🛠️ Stack Technique

L'architecture est "Serverless" et contenue localement, conformément aux contraintes de l'atelier.

- **Application :** Python (Jupyter Notebook) pour l'orchestration et la visualisation.
- **Stockage & Requêtage :** [DuckDB](https://duckdb.org/) (Base de données analytique in-process).
- **Gestion de version :** Git / GitHub.

## 📊 Le Jeu de Données (présent dans `Atelier1/Data`)

Les fichiers de données fournis avec ce dépôt correspondent à des parties de **Rocket League** (format "in-game" très détaillé). Les fichiers se trouvent dans le répertoire `Atelier1/Data` et couvrent des événements, matchs, parties et métriques par joueur.

Fichiers principaux présents :

- `Atelier1/Data/main.csv` — table centrale d'événements / parties / games (game_id, match_id, timestamps, map, duration, overtime, etc.)
- `Atelier1/Data/players_db.csv` — référence des joueurs (`player_id`, `player_slug`, `player_tag`, `player_name`, `player_country`)
- `Atelier1/Data/matches_by_players.csv` — statistiques par joueur pour chaque match (shots, goals, saves, boost, movement, positioning, advanced metrics...)
- `Atelier1/Data/matches_by_teams.csv` — statistiques agrégées par équipe et match
- `Atelier1/Data/games_by_players.csv` — granularité partie/joueur (peut être volumineux)
- `Atelier1/Data/games_by_teams.csv` — granularité partie/équipe

Caractéristiques clés :

- Granularité "in-game" : boost, puissance, temps supersonic, positionnement moyen par rapport à la balle, tirs, buts, assists, saves, etc.
- Volumétrie : plusieurs fichiers contiennent des dizaines de milliers de lignes (certaines vues `games_by_players.csv` sont volumineuses >50MB).
- Format : CSV, encodage UTF-8 (séparateur `,`).

Si vous avez une source en ligne pour ce dataset, ajoutez le lien ci‑dessous, sinon nous considérons le dataset comme inclus localement dans le dépôt.

- **Source / Lien vers le dataset :** (dataset inclus localement — ajouter un lien ici si vous en disposez)

## 🗄️ Schéma Relationnel

### ⭐ Schéma Final — **Validé par le formateur**

Le schéma utilise une **architecture normalisée** avec dimensions essentielles et une table de mapping centrale pour les statistiques :

**8 Dimensions**:

- `Country` — Pays (évite doublons)
- `Region` — Régions géographiques (évite doublons)
- `Player` — Joueurs avec `country_id` FK
- `Team` — Équipes avec `region_id` FK
- `Event` — Événements eSport avec `region_id` FK
- `Match` — Matchs avec `event_id`, `map_id` FK
- `Map` — Cartes de jeu
- `Score` — Scores par équipe/match avec résultat

**Tables de Stats (centrale + lookup)**:

- `StatMapping` — Table centrale polymorphe (entity_id + entity_type)
- `Stat` — Valeurs statistiques (stat_value, type_id FK)
- `StatType` — Types de stats (name, category)

**Architecture polymorphe:**

- `entity_type` = 'player' | 'team' | 'match'
- Permet de lier stats à différentes entités via une seule table
- `StatMapping` → `Stat` → `StatType`

**Avantages:**

- ✅ Normalisation complète (Country, Region)
- ✅ Zéro redondance géographique
- ✅ Architecture flexible et scalable
- ✅ Relations polymorphes pour extensibilité

### 📊 Fichiers du Schéma

**⭐ Schéma Validé**:

- 🖼️ [Image PNG](docs/schema_final.png) — Diagramme ER avec 8 dimensions + stat mapping
- 💾 [DDL SQL](sql/schema_final.sql) — Schéma complet avec contraintes FK
- 📊 [Code Mermaid](docs/schema_final.mmd) — Source du diagramme

---

## 🚀 Installation et Utilisation (rapide)

1.  Cloner le dépôt :

    ```bash
    git clone https://github.com/Sam-rst/EPSI_M1-Datamart
    cd EPSI_M1-Datamart/Atelier1
    ```

2.  Créer l'environnement virtuel et installer les dépendances :

    ```bash
    uv sync
    ```

3.  Lancer les notebooks ou scripts d'ingestion :
    - Ouvrez `notebooks/rocketLeague.ipynb` pour l'exploration.
    - Le script d'ingestion `scripts/load_data.py` (à créer) chargera les CSV dans DuckDB.
