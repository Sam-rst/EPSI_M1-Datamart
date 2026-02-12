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

## 🚀 Installation et Utilisation

### 📦 Prérequis

- **Python 3.11+**
- **Git**
- Gestionnaire de packages Python (pip ou uv)

### 1️⃣ Installation

1. **Cloner le dépôt** :

   ```bash
   git clone https://github.com/Sam-rst/EPSI_M1-Datamart
   cd EPSI_M1-Datamart
   ```

2. **Créer l'environnement virtuel** :

   ```bash
   # Avec uv (recommandé)
   uv sync
   
   # Ou avec pip
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Activer l'environnement** :

   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

### 2️⃣ Création de la Base de Données et Import des Données

**⚠️ ÉTAPE OBLIGATOIRE** : Avant toute analyse, vous devez créer la base DuckDB et importer les données CSV.

#### 📥 Script d'ingestion : `ingest_duckdb.py`

Ce script crée automatiquement la base `data/rl.duckdb` et importe les 6 fichiers CSV (199,117 lignes au total).

```bash
# Assurez-vous d'être dans le répertoire racine du projet
python scripts/ingest_duckdb.py
```

**Sortie attendue** :
```
🚀 Ingestion des données dans DuckDB...
   Base de données : data/rl.duckdb

✓ Table players_db créée : 1,218 lignes
✓ Table main créée : 18,740 lignes
✓ Table games_by_players créée : 106,795 lignes
✓ Table games_by_teams créée : 35,594 lignes
✓ Table matches_by_players créée : 26,176 lignes
✓ Table matches_by_teams créée : 10,594 lignes

✅ Ingestion terminée avec succès !
   Total : 199,117 lignes importées
   Taille de la base : 49.51 MB
```

**Fichier créé** : `data/rl.duckdb` (49.51 MB)

#### ✅ Vérification de l'import

Pour vérifier que les données sont bien chargées :

```bash
python scripts/validate_db.py
```

**Sortie attendue** :
```
📊 Validation de la base DuckDB...

✓ players_db : 1,218 lignes
✓ main : 18,740 lignes
✓ games_by_players : 106,795 lignes
✓ games_by_teams : 35,594 lignes
✓ matches_by_players : 26,176 lignes
✓ matches_by_teams : 10,594 lignes

✅ Base validée : 199,117 lignes au total
```

### 3️⃣ Autres Scripts Disponibles

#### 🔍 Inspection du dataset

Pour analyser les fichiers CSV avant import :

```bash
python scripts/inspect_dataset.py
```

Affiche :
- Nombre de lignes par fichier
- Colonnes et types de données
- Aperçu des premières lignes
- Statistiques de volumétrie

#### 📊 Export du schéma

Pour générer le diagramme PNG du schéma relationnel :

```bash
python scripts/export_schema_final.py
```

Génère : `docs/schema_final.png`

### 4️⃣ Utilisation du Notebook

Une fois la base créée, ouvrez le notebook d'exploration :

```bash
# Lancer Jupyter
jupyter notebook notebooks/step1_dataset_exploration.ipynb
```

**Contenu du notebook** :
- ✅ Description du dataset
- ✅ Inventaire des fichiers CSV
- ✅ Vérification de la base DuckDB
- ✅ Requêtes d'analyse (top joueurs, plateformes, etc.)

### 5️⃣ Visualisation avec DBeaver (Optionnel)

Pour explorer la base graphiquement :

1. **Télécharger DBeaver** : https://dbeaver.io/download/
2. **Créer une connexion DuckDB** :
   - Nouvelle connexion → DuckDB
   - Path : `C:\Users\<votre_user>\...\EPSI_M1-Datamart\data\rl.duckdb`
   - Test Connection → Finish
3. **Explorer les tables** : 6 tables disponibles avec 199K lignes

⚠️ **Important** : Fermez DBeaver avant d'exécuter des scripts Python qui modifient la base (problème de verrouillage de fichier).
