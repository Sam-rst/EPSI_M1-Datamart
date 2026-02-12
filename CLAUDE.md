# CLAUDE.md - Atelier 1 : Ingestion & Modélisation Relationnelle

## Contexte
Premier module du projet BI Rocket League.
Objectif : Mettre en place la stack technique "Serverless" (Python + DuckDB), concevoir le modèle relationnel (3NF) et ingérer les données brutes CSV.

## Structure des données (3NF)
[cite_start]Le schéma relationnel doit respecter la forme normale[cite: 57].
- **matches** : `match_id` (PK), date, map, duration.
- **teams** : `team_id` (PK), name, region.
- **players** : `player_id` (PK), name, `team_id` (FK).
- **game_stats** : `stat_id` (PK), `match_id` (FK), `player_id` (FK), goals, assists, saves, shots, score, winner.

## Commandes Principales
- **Installation** : `pip install -r requirements.txt`
- **Lancer l'ingestion** : `python ingestion.py`
- **Vérifier la DB** : `python -c "import duckdb; con=duckdb.connect('rocket_league.db'); print(con.sql('SHOW TABLES'));"`

## Règles de Code
- [cite_start]**Stack** : Pas de backend serveur, stockage local via DuckDB[cite: 47, 49].
- **SQL** : Utiliser `duckdb.execute()` avec du SQL pur pour la création des tables et le chargement.
- [cite_start]**Données** : Le script doit créer le schéma s'il n'existe pas et charger les données de manière idempotente (gérer les doublons)[cite: 60].
- **Chemins** : Les fichiers CSV sources sont attendus dans le dossier `data/` ou à la racine de l'atelier.

## Livrables
- Un script Python d'ingestion.
- Un fichier `rocket_league.db` (généré).
- [cite_start]Mise à jour du `README.md` avec l'ERD/MCD et la présentation du dataset[cite: 50, 58].