# Atelier 2 — Modèle dimensionnel

## Objectif

Transformer la base relationnelle normalisée (Atelier 1) en un entrepôt de données structuré en étoile pour la Business Intelligence.

## Étapes

### 1. Modélisation dimensionnelle
- Concevoir un **schéma en étoile**
- Identifier la/les **tables de faits** (mesures, événements, granularité)
- Identifier les **dimensions** : temps, joueurs, personnages/classes, cartes…
- Le modèle doit permettre des requêtes complexes (ex : taux de victoire par classe sur une carte le week-end)
- Ajouter le schéma dimensionnel au dépôt + mise à jour du README

### 2. Alimentation des dimensions
- Script SQL ou Python pour extraire les données du modèle relationnel vers les dimensions
- Gérer l'unicité des membres
- Créer des surrogate keys si nécessaire
- Nettoyer/transformer les données brutes (dates, regroupements…)

### 3. Remplissage des faits
- Script de chargement de la table de faits
- Récupérer les clés étrangères des dimensions
- Calculer/agréger les mesures (durée, scores, dégâts…)
- Assurer l'intégrité référentielle faits ↔ dimensions