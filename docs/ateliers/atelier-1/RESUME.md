# Atelier 1 — Statistiques de parties

## Objectif

Structurer, alimenter et exploiter un entrepôt de données pour analyser le détail des parties d'un jeu vidéo.

## Étapes

### 1. Jeu de données
Trouver un dataset de parties d'un jeu vidéo respectant :
- Plusieurs dizaines de milliers de parties
- Statistiques in-game (pas juste joueurs + résultat)
- Jeu à fortes interactions (pas de puzzles/jeux de plateau)

### 2. Stack technique
Mettre en place un dépôt GitHub avec une stack **sans backend** :
- Application : page web ou notebook
- Stockage : DuckDB ou SQLite (compatibles web/notebook)
- README avec : lien dataset, présentation du contenu, membres de l'équipe

### 3. Modèle relationnel
- Concevoir un ERD/MCD en forme normale pour stocker les données du dataset
- L'inclure dans le README

### 4. Chargement des données
- Script qui crée le schéma s'il n'existe pas et charge les données

## Livrable
Lien du dépôt GitHub/GitLab envoyé avant le **10/02/2026**.