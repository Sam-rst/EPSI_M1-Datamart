# Projet Datamart — Rocket League Esports

Projet d'analyse et d'entreposage de donnees pour des parties de **Rocket League** (RLCS 2021-22).
L'objectif est de structurer, charger et exploiter des statistiques in-game detaillees (mouvement, boost, positionnement, tirs, etc.).

Pipeline : `CSV (Kaggle) -> Modele relationnel 3NF (DuckDB) -> Schema en etoile -> Dashboard BI`

## Equipe

- **Samuel RESSIOT**
- **Rudolph ATTISSO**
- **Yassine ZOUITNI**

## Jeu de donnees

- **Source** : [RLCS 2021-22 — Kaggle](https://www.kaggle.com/datasets/dylanmonfret/rlcs-202122)
- **Origine** : donnees extraites d'[octane.gg](https://octane.gg)
- **Volume** : ~199 000 lignes au total

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `main.csv` | ~18 700 | Donnees game-level : events, stages, matchs, maps, durations |
| `games_by_players.csv` | ~106 000 | Stats par joueur par game (shots, goals, saves, boost, movement, positioning, demos) |
| `games_by_teams.csv` | ~35 500 | Stats agregees par equipe par game |
| `matches_by_players.csv` | ~26 000 | Stats par joueur par match (agregees) |
| `matches_by_teams.csv` | ~10 500 | Stats par equipe par match (agregees) |
| `players_db.csv` | ~1 200 | Registre des joueurs (id, tag, nom, pays) |

Colonnes de jointure cles : `game_id`, `match_id`, `player_id`, `team_id`. Couleurs : `blue` / `orange`.

## Stack technique

Architecture serverless, sans backend, conforme aux contraintes de l'atelier.

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.13 |
| Gestionnaire de paquets | [uv](https://docs.astral.sh/uv/) |
| ORM | SQLAlchemy 2.0 (DeclarativeBase, mapped_column) |
| Migrations | Alembic |
| Base de donnees | DuckDB (in-process, via duckdb-engine) |
| Configuration | python-dotenv (`.env`) |
| Data | pandas |
| Visualisation | matplotlib, seaborn |
| Presentation | Jupyter Notebook |

## Structure du projet

```
.
├── alembic/                        # Migrations Alembic
│   ├── env.py
│   └── versions/                   # Fichiers de migration
├── data/
│   ├── raw/                        # CSVs bruts Kaggle (gitignore)
│   ├── processed/                  # CSVs normalises 3NF (gitignore)
│   └── rl.duckdb                   # Base DuckDB (gitignore)
├── docs/
│   ├── ateliers/                   # Consignes et resumes par atelier
│   └── database/schemas/           # ERD et schemas (mmd, dbml, png, svg)
├── notebooks/
│   ├── 01_raw_extraction.ipynb     # Extraction du dataset Kaggle
│   ├── 02_transform.ipynb          # Transformation CSV -> 14 tables 3NF
│   └── 03_load.ipynb               # Chargement dans DuckDB via ORM
├── src/
│   ├── config.py                   # ROOT_DIR, DATA_DIR, RAW_DIR, PROCESSED_DIR, DB_PATH
│   ├── database/
│   │   ├── engine.py               # SQLAlchemy engine + SessionLocal
│   │   └── models/                 # 14 modeles ORM (5 modules)
│   └── etl/
│       ├── main.py                 # Pipeline complet (extract -> transform -> load)
│       ├── extract/                # Telechargement Kaggle + validation
│       │   ├── core/               # download, copy, ensure (idempotent)
│       │   ├── config/             # datasets, primary keys
│       │   └── utils/              # inventory, validation (PK/nulls)
│       ├── transform/              # Normalisation CSV bruts -> 14 DataFrames
│       │   ├── core/               # referentials, entities, hierarchy,
│       │   │                       # participation, stats (EAV unpivot), export
│       │   ├── config/             # columns mappings, loading functions
│       │   └── utils/              # cleaning, mapping
│       └── load/                   # Insertion DuckDB (ORM ou COPY natif)
│           ├── core/               # migrate, truncate, insert (ORM), copy (natif DuckDB)
│           ├── config/             # table order (FK-aware), chunk size, settings (.env)
│           └── utils/              # CSV readers
├── .env                           # Configuration locale (gitignore)
├── .env.example                   # Template de configuration
├── alembic.ini
├── pyproject.toml
└── uv.lock
```

## Modele relationnel (3NF) — Atelier 1

Le schema normalise comprend **14 tables** reparties en 5 groupes :

| Groupe | Tables | Description |
|--------|--------|-------------|
| Referentiels | Country, Region, Map, Car | Lookups sans dependances |
| Entites | Player, Team | Acteurs principaux |
| Hierarchie | Event > Stage > Match > Game | Decomposition des competitions |
| Participation | GamePlayer, GameTeam | Liens game-level (couleur, winner, camera settings) |
| Stats (EAV) | StatType, Stat | Stats polymorphiques (entity_type = player/team) |

**Architecture polymorphique (EAV)** : la table `Stat` utilise `entity_id` + `entity_type` pour pointer vers Player ou Team. Ajouter une nouvelle statistique = `INSERT` dans `StatType`, pas de migration de schema.

### ERD

![Schema 3NF](docs/database/schemas/schema_3nf.png)

- [Source Mermaid](docs/database/schemas/schema_3nf.mmd)
- [DBML (dbdiagram.io)](docs/database/schemas/schema_3nf.dbml)
- [SVG](docs/database/schemas/schema_3nf.svg)

## Pipeline ETL

Le pipeline complet s'execute en 3 etapes, orchestrees par les notebooks ou en CLI :

```
Kaggle (dylanmonfret/rlcs-202122)
        | [extract]
data/raw/ (6 CSVs bruts, ~199k lignes)
        | [transform]
data/processed/ (14 CSVs normalises 3NF, ~1.3 Go dont stat.csv)
        | [load]
data/rl.duckdb (14 tables, schema 3NF complet)
```

| Etape | Module | Description |
|-------|--------|-------------|
| **Extract** | `src/etl/extract/` | Telechargement Kaggle via kagglehub, copie vers `data/raw/`, validation des PK et nulls |
| **Transform** | `src/etl/transform/` | Nettoyage, normalisation, deduplication, unpivot EAV (89+ types de stats), export CSV |
| **Load** | `src/etl/load/` | Migration Alembic, truncate (idempotent), insertion ORM ou COPY natif DuckDB (configurable via `.env`) |

Chaque module est executable via notebook (`01`, `02`, `03`) ou en CLI (`python -m src.etl.extract`, etc.).

### Configuration du chargement

Le mode d'insertion est configurable dans `.env` :

```bash
# .env
LOAD_METHOD=orm   # SQLAlchemy ORM bulk insert (safe, ~20 min pour 10.5M lignes)
LOAD_METHOD=copy  # DuckDB native read_csv (rapide, ~1 min pour 10.5M lignes)
```

## Installation

### Prerequis

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Git
- Compte Kaggle (pour le telechargement automatique du dataset)

### Setup

```bash
# 1. Cloner le depot
git clone https://github.com/Sam-rst/EPSI_M1-Datamart
cd EPSI_M1-Datamart

# 2. Installer les dependances
uv sync

# 3. Configurer l'environnement
cp .env.example .env              # Puis editer .env si besoin

# 4. Pipeline complet (via notebooks ou CLI)
# Option A : ouvrir les notebooks dans l'ordre (01 -> 02 -> 03)
jupyter notebook

# Option B : CLI (pipeline complet)
uv run python -m src.etl              # Tout en une commande

# Option C : CLI (etape par etape)
uv run python -m src.etl.extract     # Telecharger les CSVs bruts
uv run python -m src.etl.transform   # Normaliser en 14 tables
uv run python -m src.etl.load        # Charger dans DuckDB
```

### Commandes utiles

```bash
# Migrations Alembic
uv run alembic upgrade head           # Appliquer toutes les migrations
uv run alembic history                # Historique des migrations
uv run alembic revision -m "msg"      # Nouvelle migration (manuelle)
uv run alembic downgrade -1           # Rollback derniere migration
```

## Avancement par atelier

### Atelier 1 — Statistiques de parties

| Etape | Statut | Detail |
|-------|--------|--------|
| Jeu de donnees | Fait | RLCS 2021-22 via Kaggle (~199k lignes, 6 CSVs) |
| Stack technique | Fait | Python 3.13 + uv + DuckDB + SQLAlchemy 2.0 + Jupyter |
| Modele relationnel | Fait | 14 tables 3NF, ERD Mermaid + DBML + PNG + SVG |
| ETL Extract | Fait | Telechargement Kaggle, validation PK/nulls, inventaire |
| ETL Transform | Fait | Normalisation 14 tables, unpivot EAV (89+ stat types), export CSV |
| ETL Load | Fait | Migration Alembic, insertion ORM ou COPY natif DuckDB (`.env`), verification SQL |
| Notebooks | Fait | 01_extract, 02_transform, 03_load — pipeline complet |

### Atelier 2 — Modele dimensionnel

| Etape | Statut | Detail |
|-------|--------|--------|
| Schema en etoile | A faire | fact_game_stats + dimensions |
| Alimentation des dimensions | A faire | Script Python/SQL |
| Remplissage des faits | A faire | Script Python/SQL |

### Atelier 3 — Visualisation

| Etape | Statut | Detail |
|-------|--------|--------|
| 5+ KPIs (2 simples + 2 croisees) | A faire | |
| 2 filtres interactifs | A faire | |
| Export CSV | A faire | |
