# Data Engineer - Rocket League Data Warehouse

## Identité du rôle
**Responsable**: Pipelines de données et qualité des données
**Objectif principal**: Ingérer, transformer et préparer les données pour l'analyse

---

## Responsabilités principales

### 1. Ingestion des données (Atelier 1)
- Télécharger et organiser les données brutes depuis Kaggle
- Créer le schéma relationnel 3NF dans DuckDB
- Implémenter le script `ingestion.py` avec gestion des doublons
- Valider l'intégrité et la qualité des données ingérées

### 2. Transformation des données (Atelier 2)
- Concevoir les transformations vers le modèle dimensionnel
- Créer les tables de faits et dimensions
- Implémenter les calculs de métriques dérivées
- Optimiser les performances des requêtes analytiques

### 3. Qualité des données
- Détecter et gérer les valeurs manquantes
- Identifier les anomalies et outliers
- Documenter les règles de qualité appliquées
- Mettre en place des contrôles de cohérence

### 4. Documentation des données
- Décrire la structure des fichiers sources
- Documenter les transformations appliquées
- Maintenir un data dictionary (dictionnaire de données)
- Tracer la lignée des données (data lineage)

---

## Livrables attendus

### Atelier 1 - Ingestion
- [x] `scripts/ingestion.py` : Script d'ingestion complet
- [ ] `rocket_league.db` : Base DuckDB avec données chargées
- [ ] `data/raw/` : Données sources organisées
- [ ] Documentation des sources et de la structure

### Atelier 2 - Modélisation
- [ ] `scripts/modeling.py` : Transformations vers le modèle star
- [ ] Tables dimensionnelles créées
- [ ] Tables de faits créées
- [ ] Requêtes de validation

### Atelier 3 - Préparation analytics
- [ ] Agrégations pré-calculées si nécessaire
- [ ] Vues SQL pour le dashboard
- [ ] Documentation des métriques business

---

## Structure des données

### Données sources (Kaggle)
Fichiers CSV disponibles dans `data/raw/` :
- `main.csv` : Dataset principal avec toutes les informations
- `matches_by_players.csv` : Stats par joueur et par match
- `matches_by_teams.csv` : Stats par équipe et par match
- `games_by_players.csv` : Stats détaillées par game
- `games_by_teams.csv` : Stats par équipe et par game
- `players_db.csv` : Base de données des joueurs

### Schéma relationnel (3NF) - Atelier 1

#### Table `matches`
```sql
match_id VARCHAR PRIMARY KEY
date DATE
map_name VARCHAR
duration INTEGER
event_name VARCHAR
```

#### Table `teams`
```sql
team_id VARCHAR PRIMARY KEY
team_name VARCHAR
region VARCHAR
```

#### Table `players`
```sql
player_id VARCHAR PRIMARY KEY
player_name VARCHAR
team_id VARCHAR (FK → teams.team_id)
```

#### Table `game_stats`
```sql
stat_id INTEGER PRIMARY KEY
match_id VARCHAR (FK → matches.match_id)
player_id VARCHAR (FK → players.player_id)
goals INTEGER
assists INTEGER
saves INTEGER
shots INTEGER
score INTEGER
winner BOOLEAN
```

---

## Scripts et code

### `scripts/ingestion.py` - Structure actuelle
```python
import duckdb
import pandas as pd

# Connexion persistante
con = duckdb.connect('rocket_league.db')

def create_relational_schema():
    """Crée les 4 tables en 3NF"""
    # CREATE TABLE IF NOT EXISTS...

def load_data():
    """Charge les données depuis CSV"""
    # INSERT OR IGNORE pour idempotence

if __name__ == "__main__":
    create_relational_schema()
    load_data()
    con.close()
```

### Améliorations à envisager
- [ ] Ajouter des logs de progression
- [ ] Gérer les erreurs avec try/except
- [ ] Ajouter des validations de qualité
- [ ] Créer des fonctions pour chaque table
- [ ] Ajouter des statistiques de chargement

---

## Interactions avec les autres rôles

### Avec le Tech Lead
- **Reçoit** : Spécifications du schéma, standards de code
- **Demande** : Validation technique, revue de code
- **Propose** : Optimisations, solutions techniques

### Avec le Project Manager
- **Informe** : Avancement, blocages, problèmes de qualité
- **Reçoit** : Priorisation des tâches
- **Alerte** : Risques liés aux données (qualité, volumétrie)

---

## Checklist Atelier 1

### Préparation des données
- [x] Téléchargement du dataset Kaggle RLCS 2021-22
- [x] Organisation des fichiers dans `data/raw/`
- [ ] Exploration initiale des données (notebook)
- [ ] Identification des colonnes clés

### Implémentation
- [x] Script `ingestion.py` créé
- [x] Fonction `create_relational_schema()` implémentée
- [x] Fonction `load_data()` implémentée
- [ ] Gestion robuste des erreurs
- [ ] Tests de l'idempotence (double exécution)

### Validation
- [ ] Vérifier le nombre de lignes par table
- [ ] Contrôler l'intégrité référentielle
- [ ] Valider les types de données
- [ ] Détecter les valeurs manquantes
- [ ] Comparer avec les données sources

### Documentation
- [ ] Documenter les choix de chargement
- [ ] Ajouter des exemples de requêtes
- [ ] Créer un data dictionary

---

## Commandes utiles

### Installation des dépendances
```bash
pip install -r requirements.txt
# ou avec uv
uv sync
```

### Exécution de l'ingestion
```bash
cd scripts
python ingestion.py
```

### Vérification de la base
```bash
python -c "import duckdb; con=duckdb.connect('rocket_league.db'); print(con.sql('SHOW TABLES').fetchall())"
```

### Requêtes de validation
```sql
-- Compter les lignes par table
SELECT COUNT(*) FROM matches;
SELECT COUNT(*) FROM teams;
SELECT COUNT(*) FROM players;
SELECT COUNT(*) FROM game_stats;

-- Vérifier l'intégrité référentielle
SELECT COUNT(*) FROM players WHERE team_id NOT IN (SELECT team_id FROM teams);
SELECT COUNT(*) FROM game_stats WHERE match_id NOT IN (SELECT match_id FROM matches);
```

---

## Bonnes pratiques

### Gestion des erreurs
- Utiliser `try/except` pour les opérations critiques
- Logger les erreurs dans un fichier
- Fournir des messages d'erreur clairs

### Performance
- Utiliser `INSERT OR IGNORE` pour l'idempotence
- Préférer les requêtes SQL bulk aux insertions ligne par ligne
- Indexer les colonnes utilisées dans les jointures

### Qualité
- Valider les types de données
- Gérer les valeurs NULL de manière explicite
- Documenter les hypothèses et transformations
- Tester sur un échantillon avant de charger tout le dataset

### Reproductibilité
- Rendre le script exécutable plusieurs fois sans erreur
- Documenter les dépendances (versions)
- Utiliser des chemins relatifs, pas absolus
