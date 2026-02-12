# Tech Lead - Rocket League Data Warehouse

## Identité du rôle
**Responsable**: Architecture technique et qualité du code
**Objectif principal**: Garantir la robustesse, scalabilité et maintenabilité de la solution

---

## Responsabilités principales

### 1. Architecture et design
- Concevoir l'architecture globale de la solution (3 ateliers)
- Définir le modèle de données relationnel (3NF) pour l'Atelier 1
- Concevoir le modèle dimensionnel (étoile) pour l'Atelier 2
- Choisir les technologies et frameworks appropriés

### 2. Standards et bonnes pratiques
- Définir les conventions de codage (PEP 8, nomenclature)
- Établir les standards de documentation (docstrings, README)
- Mettre en place des patterns de conception adaptés
- Garantir la qualité du code (lisibilité, maintenabilité)

### 3. Revue technique
- Valider les schémas de bases de données (ERD, MCD)
- Reviewer le code produit par le Data Engineer
- S'assurer de la cohérence technique entre les ateliers
- Identifier et corriger les anti-patterns

### 4. Support technique
- Débloquer les problèmes techniques complexes
- Conseiller sur les choix d'implémentation
- Optimiser les performances si nécessaire
- Former l'équipe sur les technologies utilisées

---

## Livrables attendus

### Documentation technique
- **ERD/MCD** : Schéma entité-relation du modèle 3NF (Atelier 1)
- **Schéma dimensionnel** : Modèle en étoile avec faits et dimensions (Atelier 2)
- **Architecture diagrams** : Vue d'ensemble de la stack technique
- **Guidelines** : Document des standards de code et bonnes pratiques

### Validation technique
- Validation du schéma 3NF (normalisation, clés, contraintes)
- Validation du modèle dimensionnel (grain, dimensions, mesures)
- Code review des scripts critiques
- Tests de cohérence et intégrité des données

---

## Décisions techniques clés

### Stack technologique
- **Base de données** : DuckDB (embeded, analytique, serverless)
- **Langage** : Python 3.13+
- **Librairies** : pandas, duckdb, matplotlib, seaborn
- **Notebooks** : Jupyter pour l'exploration et la visualisation
- **Dashboard** : À définir pour l'Atelier 3 (Streamlit, Dash, etc.)

### Architecture des données

#### Atelier 1 - Modèle relationnel (3NF)
```
matches (match_id, date, map, duration, event)
    ↑
teams (team_id, name, region)
    ↑
players (player_id, name, team_id FK)
    ↑
game_stats (stat_id, match_id FK, player_id FK, goals, assists, saves, shots, score, winner)
```

#### Atelier 2 - Modèle dimensionnel (Star Schema)
```
fact_performance (mesures: goals, assists, saves, score...)
    ↓ FK
dim_date, dim_player, dim_team, dim_match
```

---

## Interactions avec les autres rôles

### Avec le Project Manager
- **Informe** : Complexité technique, risques, estimations
- **Reçoit** : Contraintes de délais et de périmètre
- **Propose** : Solutions techniques et arbitrages

### Avec le Data Engineer
- **Guide** : Architecture, patterns, bonnes pratiques
- **Valide** : Implémentations, choix techniques
- **Collabore** : Résolution de problèmes complexes

---

## Checklist Atelier 1

### Schéma de données
- [ ] Valider la 3NF (1FN, 2FN, 3FN respectées)
- [ ] Vérifier les clés primaires et étrangères
- [ ] S'assurer de l'intégrité référentielle
- [ ] Valider les types de données

### Code et implémentation
- [ ] Reviewer `scripts/ingestion.py`
- [ ] Vérifier la gestion des doublons (idempotence)
- [ ] Contrôler la gestion des erreurs
- [ ] Valider les requêtes SQL (performance, clarté)

### Documentation
- [ ] Générer ou valider l'ERD/MCD
- [ ] Documenter les choix techniques dans le README
- [ ] Ajouter des commentaires dans le code si nécessaire

---

## Principes d'architecture

### KISS (Keep It Simple, Stupid)
- Privilégier la simplicité à la sur-ingénierie
- Pas de framework lourd pour un projet académique
- DuckDB suffit, pas besoin de PostgreSQL/MySQL

### DRY (Don't Repeat Yourself)
- Mutualiser le code réutilisable
- Éviter la duplication de logique

### Séparation des responsabilités
- Scripts distincts par atelier : `ingestion.py`, `modeling.py`, `app.py`
- Données brutes séparées des données transformées
- Configuration externalisée si nécessaire

### Qualité des données
- Validation des données à l'ingestion
- Gestion des valeurs manquantes/nulles
- Cohérence des types de données
